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

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(''.join(str(b) for b in byte), 2)) for byte in chars)

def main():
    # Đọc bản mã và khóa từ file
    with open("ciphertext.txt", "r") as f:
        ciphertext_bits = [int(bit) for bit in f.read().strip()]
    with open("key.txt", "r") as f:
        key = f.read().strip()

    # Khởi tạo các thanh ghi với khóa đã lưu
    R1, R2, R3 = initialize_lfsrs(key)

    # Tạo chuỗi keystream với độ dài bằng bản mã
    keystream = generate_keystream(R1, R2, R3, len(ciphertext_bits))

    # Giải mã bản mã
    decrypted_bits = xor_data(ciphertext_bits, keystream)
    decrypted_text = bits_to_text(decrypted_bits)
    print(f"Bản rõ sau khi giải mã: {decrypted_text}")

if __name__ == "__main__":
    main()
