def initialize_lfsrs(key):
    assert len(key) == 64, "Khóa phải là chuỗi nhị phân 64-bit"
    R1 = [int(bit) for bit in key[:19]]
    R2 = [int(bit) for bit in key[19:41]]
    R3 = [int(bit) for bit in key[41:]]
    return R1, R2, R3

def majority(x, y, z):
    return (x & y) | (x & z) | (y & z)

def clock_lfsr(lfsr, feedback_bits):
    feedback_bits = [bit for bit in feedback_bits if bit < len(lfsr)]
    feedback = 0
    for bit in feedback_bits:
        feedback ^= lfsr[bit]
    lfsr = [feedback] + lfsr[:-1]
    return lfsr

def generate_keystream(R1, R2, R3, keystream_length):
    keystream = []
    for _ in range(keystream_length):
        majority_bit = majority(R1[8], R2[10], R3[10])
        if R1[8] == majority_bit:
            R1 = clock_lfsr(R1, [13, 16, 17, 18])
        if R2[10] == majority_bit:
            R2 = clock_lfsr(R2, [20, 21])
        if R3[10] == majority_bit:
            R3 = clock_lfsr(R3, [7, 20, 21, 22])
        keystream_bit = R1[-1] ^ R2[-1] ^ R3[-1]
        keystream.append(keystream_bit)
    return keystream

def xor_data(data, keystream):
    return [bit ^ keystream[i % len(keystream)] for i, bit in enumerate(data)]

def text_to_bits(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def main():
    # Bước 1: Nhập thông tin bản rõ
    name = input("Nhập họ và tên: ")
    student_id = input("Nhập mã số sinh viên: ")
    student_class = input("Nhập lớp: ")
    plaintext = "{}, {}, {}".format(name, student_id, student_class)
    
    # Chuyển bản rõ thành nhị phân
    plaintext_bits = text_to_bits(plaintext)
    print(f"Bản rõ dạng nhị phân: {plaintext_bits}")
    
    # Bước 2: Nhập khóa K
    key = input("Nhập khóa K (64-bit nhị phân): ")
    R1, R2, R3 = initialize_lfsrs(key)
    
    # Tạo chuỗi keystream
    keystream = generate_keystream(R1, R2, R3, len(plaintext_bits))
    
    # Mã hóa bản rõ
    ciphertext_bits = xor_data(plaintext_bits, keystream)
    print(f"Bản mã dạng nhị phân: {ciphertext_bits}")
    
    # Lưu bản mã và khóa vào file
    with open("ciphertext.txt", "w") as f:
        f.write(''.join(map(str, ciphertext_bits)))
    with open("key.txt", "w") as f:
        f.write(key)

    print("Bản mã và khóa đã được lưu vào file.")

if __name__ == "__main__":
    main()
