from django import template
from django.shortcuts import render
from django.http import JsonResponse
from geffe_cipher import GeffeCipher, encrypt_message, decrypt_message
import json

register = template.Library()

def home(request):
    return render(request, 'cipher_app/home.html')

def cipher(request):
    return render(request, 'cipher_app/index.html')

def process_text(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text', '')
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)
                
            action = request.POST.get('action', '')
            if action not in ['encrypt', 'decrypt']:
                return JsonResponse({'error': 'Invalid action'}, status=400)

            # Initial states and tap positions
            lfsr1_init = [1, 0, 1, 0, 1]  # 5-bit
            lfsr1_taps = [0, 2]
            
            lfsr2_init = [1, 1, 0, 0, 1, 0, 1]  # 7-bit
            lfsr2_taps = [0, 1]
            
            lfsr3_init = [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]  # 11-bit
            lfsr3_taps = [0, 2]
            
            class DetailedGeffeCipher(GeffeCipher):
                def step(self):
                    # LFSR1 step
                    x1 = self.lfsr1.step()
                    # LFSR2 step
                    x2 = self.lfsr2.step()
                    # LFSR3 step
                    x3 = self.lfsr3.step()
                    # Calculate combined output
                    term1 = x1 & x2  # First AND operation
                    not_x3 = 1 ^ x3  # NOT operation on x3
                    term2 = x2 & not_x3  # Second AND operation
                    result = term1 ^ term2  # Final XOR operation
                    # Store step information
                    step_info = {
                        'lfsr1_output': x1,
                        'lfsr2_output': x2,
                        'lfsr3_output': x3,
                        'term1': term1,
                        'not_x3': not_x3,
                        'term2': term2,
                        'result': result
                    }
                    return result, step_info
                def generate_keystream(self, length):
                    """Generate keystream of specified length with detailed step information"""
                    keystream = []
                    steps_info = []
                    for _ in range(length):
                        bit, step_info = self.step()
                        keystream.append(bit)
                        steps_info.append(step_info)
                    return keystream, steps_info

            geffe = DetailedGeffeCipher(lfsr1_init, lfsr1_taps, lfsr2_init, lfsr2_taps, lfsr3_init, lfsr3_taps)
            
            if action == 'encrypt':
                try:
                    keystream, steps_info = geffe.generate_keystream(len(text) * 8)
                    encrypted_bits = encrypt_message(text, keystream)
                    # Format the outputs
                    formatted_result = ''.join(map(str, encrypted_bits))
                    formatted_keystream = ''.join(map(str, keystream))
                    
                    # Collect LFSR outputs and operations
                    lfsr_outputs = {
                        'lfsr1': ''.join(str(step['lfsr1_output']) for step in steps_info),
                        'lfsr2': ''.join(str(step['lfsr2_output']) for step in steps_info),
                        'lfsr3': ''.join(str(step['lfsr3_output']) for step in steps_info),
                        'term1_and': ''.join(str(step['term1']) for step in steps_info),
                        'not_x3': ''.join(str(step['not_x3']) for step in steps_info),
                        'term2_and': ''.join(str(step['term2']) for step in steps_info),
                        'final_xor': formatted_keystream
                    }
                    
                    return JsonResponse({
                        'result': formatted_result,
                        'keystream': formatted_keystream,
                        'lfsr_outputs': lfsr_outputs
                    })
                except Exception as e:
                    return JsonResponse({
                        'error': f'Encryption failed: {str(e)}'
                    }, status=500)
            else:  # decrypt
                try:
                    # Convert input string of bits to list of integers
                    binary_input = [int(bit) for bit in text.replace(' ', '')]
                    keystream, steps_info = geffe.generate_keystream(len(binary_input))
                    decrypted_text = decrypt_message(binary_input, keystream)
                    # Format the outputs
                    formatted_keystream = ''.join(map(str, keystream))
                    # Collect LFSR outputs and operations
                    lfsr_outputs = {
                        'lfsr1': ''.join(str(step['lfsr1_output']) for step in steps_info),
                        'lfsr2': ''.join(str(step['lfsr2_output']) for step in steps_info),
                        'lfsr3': ''.join(str(step['lfsr3_output']) for step in steps_info),
                        'term1_and': ''.join(str(step['term1']) for step in steps_info),
                        'not_x3': ''.join(str(step['not_x3']) for step in steps_info),
                        'term2_and': ''.join(str(step['term2']) for step in steps_info),
                        'final_xor': formatted_keystream
                    }
                    return JsonResponse({
                        'result': decrypted_text,
                        'keystream': formatted_keystream,
                        'lfsr_outputs': lfsr_outputs
                    })
                except Exception as e:
                    return JsonResponse({
                        'error': f'Decryption failed: {str(e)}'
                    }, status=500)
                    
        except Exception as e:
            return JsonResponse({
                'error': f'An error occurred: {str(e)}'
            }, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
