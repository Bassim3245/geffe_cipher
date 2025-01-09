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
            action = request.POST.get('action', '')
            
            # Initial states and tap positions
            lfsr1_init = [1, 0, 1, 0, 1]  # 5-bit
            lfsr1_taps = [0, 2]
            
            lfsr2_init = [1, 1, 0, 0, 1, 0, 1]  # 7-bit
            lfsr2_taps = [0, 1]
            
            lfsr3_init = [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]  # 11-bit
            lfsr3_taps = [0, 2]
            
            # Create process information dictionary
            process_info = {
                'initial_states': {
                    'lfsr1': {'state': lfsr1_init, 'taps': lfsr1_taps},
                    'lfsr2': {'state': lfsr2_init, 'taps': lfsr2_taps},
                    'lfsr3': {'state': lfsr3_init, 'taps': lfsr3_taps}
                },
                'steps': []
            }
            
            class DetailedGeffeCipher(GeffeCipher):
                def step(self):
                    # LFSR1 step
                    lfsr1_state = self.lfsr1.state.copy()
                    lfsr1_feedback = 0
                    for tap in self.lfsr1.tap_positions:
                        lfsr1_feedback ^= lfsr1_state[tap]
                    x1 = lfsr1_state[-1]
                    
                    # LFSR2 step
                    lfsr2_state = self.lfsr2.state.copy()
                    lfsr2_feedback = 0
                    for tap in self.lfsr2.tap_positions:
                        lfsr2_feedback ^= lfsr2_state[tap]
                    x2 = lfsr2_state[-1]
                    
                    # LFSR3 step
                    lfsr3_state = self.lfsr3.state.copy()
                    lfsr3_feedback = 0
                    for tap in self.lfsr3.tap_positions:
                        lfsr3_feedback ^= lfsr3_state[tap]
                    x3 = lfsr3_state[-1]
                    
                    # Calculate combined output
                    term1 = x1 & x2
                    term2 = x2 & (1 ^ x3)
                    result = term1 ^ term2
                    
                    # Store step information
                    step_info = {
                        'lfsr1': {
                            'state': lfsr1_state,
                            'feedback': lfsr1_feedback,
                            'output': x1
                        },
                        'lfsr2': {
                            'state': lfsr2_state,
                            'feedback': lfsr2_feedback,
                            'output': x2
                        },
                        'lfsr3': {
                            'state': lfsr3_state,
                            'feedback': lfsr3_feedback,
                            'output': x3
                        },
                        'combination': {
                            'term1': term1,
                            'term2': term2,
                            'result': result
                        }
                    }
                    process_info['steps'].append(step_info)
                    
                    # Call parent's step method to actually update states
                    return super().step()
            
            geffe = DetailedGeffeCipher(lfsr1_init, lfsr1_taps, lfsr2_init, lfsr2_taps, lfsr3_init, lfsr3_taps)
            
            if action == 'encrypt':
                keystream = geffe.generate_keystream(len(text) * 8)
                encrypted_bits = encrypt_message(text, keystream)
                result = ''.join(map(str, encrypted_bits))
                return JsonResponse({
                    'result': result,
                    'process_info': process_info,
                    'keystream': ''.join(map(str, keystream))
                })
                
            elif action == 'decrypt':
                try:
                    cipher_bits = [int(bit) for bit in text.strip()]
                    keystream = geffe.generate_keystream(len(cipher_bits))
                    result = decrypt_message(cipher_bits, keystream)
                    return JsonResponse({
                        'result': result,
                        'process_info': process_info,
                        'keystream': ''.join(map(str, keystream))
                    })
                except ValueError as e:
                    return JsonResponse({'error': str(e)}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)
