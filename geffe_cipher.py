class LFSR:
    def __init__(self, initial_state, tap_positions):
        """
        تهيئة سجل الإزاحة الخطي مع التغذية الراجعة
        :param initial_state: الحالة الأولية للسجل (قائمة من 0 و 1)
        :param tap_positions: مواقع التغذية الراجعة (قائمة من المواقع)
        """
        self.state = initial_state
        self.tap_positions = tap_positions
        self.length = len(initial_state)

    def step(self):
        """
        تنفيذ خطوة واحدة من LFSR وإرجاع البت الناتج
        """
        # حساب بت التغذية الراجعة
        feedback = 0
        for tap in self.tap_positions:
            feedback ^= self.state[tap]
        
        # تخزين البت الأخير قبل الإزاحة
        output = self.state[-1]
        
        # إزاحة السجل وإضافة بت التغذية الراجعة
        for i in range(self.length-1, 0, -1):
            self.state[i] = self.state[i-1]
        self.state[0] = feedback
        
        return output

class GeffeCipher:
    def __init__(self, lfsr1_init, lfsr1_taps, lfsr2_init, lfsr2_taps, lfsr3_init, lfsr3_taps):
        """
        تهيئة نظام Geffe Cipher مع ثلاثة سجلات LFSR
        """
        self.lfsr1 = LFSR(lfsr1_init, lfsr1_taps)
        self.lfsr2 = LFSR(lfsr2_init, lfsr2_taps)
        self.lfsr3 = LFSR(lfsr3_init, lfsr3_taps)

    def step(self):
        """
        تنفيذ خطوة واحدة من خوارزمية Geffe وإرجاع البت الناتج
        """
        x1 = self.lfsr1.step()
        x2 = self.lfsr2.step()
        x3 = self.lfsr3.step()
        
        # معادلة Geffe: (x1 AND x2) XOR ((NOT x1) AND x3)
        return (x1 & x2) ^ ((1 ^ x1) & x3)

    def generate_keystream(self, length):
        """
        توليد سلسلة مفاتيح بطول محدد
        """
        return [self.step() for _ in range(length)]

def encrypt_message(message, keystream):
    """
    تشفير الرسالة باستخدام سلسلة المفاتيح
    """
    # تحويل الرسالة إلى قائمة من البتات
    message_bits = []
    for char in message:
        bits = bin(ord(char))[2:].zfill(8)
        message_bits.extend([int(bit) for bit in bits])
    
    # XOR بين الرسالة وسلسلة المفاتيح
    cipher_bits = [message_bits[i] ^ keystream[i] for i in range(len(message_bits))]
    return cipher_bits

def decrypt_message(cipher_bits, keystream):
    """
    فك تشفير الرسالة باستخدام سلسلة المفاتيح
    """
    # XOR بين النص المشفر وسلسلة المفاتيح
    message_bits = [cipher_bits[i] ^ keystream[i] for i in range(len(cipher_bits))]
    
    # تحويل البتات إلى نص
    message = ""
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        char = chr(int(''.join(map(str, byte)), 2))
        message += char
    return message

# مثال على استخدام النظام
def main():
    # تهيئة الحالات الأولية ومواقع التغذية الراجعة لكل LFSR
    lfsr1_init = [1, 0, 1, 0, 1]  # 5-bit LFSR
    lfsr1_taps = [0, 2]  # x^5 + x^3 + 1
    
    lfsr2_init = [1, 1, 0, 0, 1]  # 5-bit LFSR
    lfsr2_taps = [0, 1]  # x^5 + x^2 + 1
    
    lfsr3_init = [1, 1, 1, 0, 0]  # 5-bit LFSR
    lfsr3_taps = [0, 3]  # x^5 + x^4 + 1

    # إنشاء كائن Geffe Cipher
    geffe = GeffeCipher(lfsr1_init, lfsr1_taps, lfsr2_init, lfsr2_taps, lfsr3_init, lfsr3_taps)

    # الرسالة المراد تشفيرها
    message = "Hello, World!"
    print("Original message:", message)

    # توليد سلسلة المفاتيح
    keystream = geffe.generate_keystream(len(message) * 8)

    # تشفير الرسالة
    encrypted = encrypt_message(message, keystream)
    print("Encrypted message (bits):", ''.join(map(str, encrypted)))

    # فك تشفير الرسالة
    decrypted = decrypt_message(encrypted, keystream)
    print("Decrypted message:", decrypted)

if __name__ == "__main__":
    main()
