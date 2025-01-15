class LFSR:
    def __init__(self, initial_state, tap_positions):
        self.state = initial_state.copy()  # Make a copy to preserve initial state
        self.initial_state = initial_state.copy()  # Store initial state
        self.tap_positions = tap_positions
        self.length = len(initial_state)
    def step(self):
        # Calculate feedback
        feedback = 0
        for tap in self.tap_positions:
            feedback ^= self.state[tap]
        # Get output
        # print(self.state[-1])
        output = self.state[-1]
        # Shift register
        # print(output)
        for i in range(self.length-1, 0, -1):
            self.state[i] = self.state[i-1]
        self.state[0] = feedback
        # print(output)
        return output
class GeffeCipher:
    def __init__(self, lfsr1_init, lfsr1_taps, lfsr2_init, lfsr2_taps, lfsr3_init, lfsr3_taps):
        """
        Initialize Geffe Cipher with three LFSRs:
        LFSR1: 5-bit register
        LFSR2: 7-bit register
        LFSR3: 11-bit register
        """
        if len(lfsr1_init) != 5 or len(lfsr2_init) != 7 or len(lfsr3_init) != 11:
            raise ValueError("LFSR1 must be 5-bit, LFSR2 must be 7-bit, and LFSR3 must be 11-bit")
        self.lfsr1 = LFSR(lfsr1_init, lfsr1_taps)
        self.lfsr2 = LFSR(lfsr2_init, lfsr2_taps)
        self.lfsr3 = LFSR(lfsr3_init, lfsr3_taps)
    def step(self):
        """
        Execute one step of the Geffe algorithm and return the output bit
        Formula: (LFSR1 AND LFSR2) XOR (LFSR2 AND (NOT LFSR3))
        """
        x1 = self.lfsr1.step()
        x2 = self.lfsr2.step()
        x3 = self.lfsr3.step()
        # First term: LFSR1 AND LFSR2
        term1 = x1 & x2
        # Second term: LFSR2 AND (NOT LFSR3)
        not_x3 = 1 ^ x3
        term2 = x2 & not_x3
        # Final output
        result = term1 ^ term2
        return result
    def generate_keystream(self, length):
        """
        Generate keystream of specified length
        """
        return [self.step() for _ in range(length)]

def encrypt_message(message, keystream):
    """
    Encrypt the message using the keystream
    """
    # Convert the message to a list of bits
    message_bits = []
    for char in message:
        bits = bin(ord(char))[2:].zfill(8)
        message_bits.extend([int(bit) for bit in bits])
    
    # XOR message bits with keystream
    if len(message_bits) != len(keystream):
        raise ValueError("Message length and keystream length must match")
    
    return [message_bit ^ keystream_bit for message_bit, keystream_bit in zip(message_bits, keystream)]

def decrypt_message(cipher_bits, keystream):
    """
    Decrypt the message using the keystream
    """
    if len(cipher_bits) != len(keystream):
        raise ValueError("Cipher length and keystream length must match")
    
    # XOR cipher bits with keystream to get original message bits
    message_bits = [cipher_bit ^ keystream_bit for cipher_bit, keystream_bit in zip(cipher_bits, keystream)]
    
    # Convert bits back to characters
    message = ""
    for i in range(0, len(message_bits), 8):
        byte_bits = message_bits[i:i+8]
        char_code = int(''.join(map(str, byte_bits)), 2)
        message += chr(char_code)
    
    return message

# Example usage
def main():
    # Initialize states and tap positions for each LFSR
    lfsr1_init = [1, 0, 1, 0, 1]  # 5-bit LFSR
    lfsr1_taps = [0, 2]  # Example taps for 5-bit LFSR
    
    lfsr2_init = [1, 1, 0, 0, 1, 0, 1]  # 7-bit LFSR
    lfsr2_taps = [0, 1]  # Example taps for 7-bit LFSR
    
    lfsr3_init = [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]  # 11-bit LFSR
    lfsr3_taps = [0, 2]  # Example taps for 11-bit LFSR

    print("\n=== Geffe Cipher Demonstration ===")
    print("\nInitial Configuration:")
    print(f"LFSR1 (5-bit):  Initial state: {lfsr1_init}, Taps: {lfsr1_taps}")
    print(f"LFSR2 (7-bit):  Initial state: {lfsr2_init}, Taps: {lfsr2_taps}")
    print(f"LFSR3 (11-bit): Initial state: {lfsr3_init}, Taps: {lfsr3_taps}")
    # Create Geffe Cipher instance
    geffe = GeffeCipher(lfsr1_init, lfsr1_taps, lfsr2_init, lfsr2_taps, lfsr3_init, lfsr3_taps)
    # Message to be encrypted
    message = "Hello"
    print(f"\nOriginal message: {message}")
    # Generate keystream
    print("\nGenerating keystream...")
    keystream = geffe.generate_keystream(len(message) * 8)
    print(f"Generated keystream: {''.join(map(str, keystream))}")

    # Encrypt the message
    encrypted = encrypt_message(message, keystream)
    print(f"Encrypted message (bits): {''.join(map(str, encrypted))}")

    # Decrypt the message
    decrypted = decrypt_message(encrypted, keystream)
    print(f"Decrypted message: {decrypted}")

if __name__ == "__main__":
    main()
