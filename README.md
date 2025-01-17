# Geffe Cipher Project

## 1. Overview of Geffe Cipher
The **Geffe Cipher** is an encryption algorithm that leverages three Linear Feedback Shift Registers (**LFSRs**) to generate a ciphered sequence. This algorithm works as follows:

### Components of the Algorithm:
1. **LFSR (Linear Feedback Shift Register):**
   - A register containing bits updated periodically.
   - Uses specific tap positions for feedback.
   - Produces a sequence of bits that appear random but are deterministic.

2. **Core Process:**
   - Utilizes three LFSRs of varying lengths:
     - **LFSR1:** 5 bits.
     - **LFSR2:** 7 bits.
     - **LFSR3:** 11 bits.
   - At each step, each register outputs one bit.
   - These bits are passed to a **Boolean function**, which combines them to produce the final output.

3. **Final Output:**
   - The output of the Boolean function is used to encrypt data.

---

## 2. Project Components

### Project Structure:
1. **Core Algorithm:**
   - Implemented in a Python file named `geffe_cipher.py`.

2. **User Interface:**
   - Built using the Django framework to provide an interactive graphical user interface (GUI).
   - Includes:
     - A Django application named `cipher_app`.
     - A `templates` folder for storing HTML files for the front-end.

3. **Technologies Used:**
   - **Python 3.12**
   - **Django** (Web framework)
   - **HTML/CSS/JavaScript** (Frontend)

---

## 3. How the Algorithm Works

### Steps:
1. **Initialize Registers:**
   - Set initial values and tap positions for each register:
     - **LFSR1:** 5 bits with tap positions [0, 2].
     - **LFSR2:** 7 bits with tap positions [0, 3].
     - **LFSR3:** 11 bits with tap positions [0, 5].

2. **Encryption Process:**
   - At each step:
     1. Each register produces one bit based on its feedback configuration.
     2. The three bits are combined using a Boolean function, e.g.,:
        ```
        Z = (LFSR1 AND LFSR2) XOR (NOT LFSR1 AND LFSR3)
        ```
     3. The result, `Z`, is used to encrypt the original text.

3. **Decryption:**
   - Uses the same registers and Boolean function, along with the initial conditions, to decrypt the ciphered text.

---

## 4. Running the Project

### Requirements:
1. Install Python 3.12.
2. Install Django using the command:
   ```bash
   pip install django
   ```

### Steps to Run:
1. Open a terminal and navigate to the project directory.
2. Start the local server using:
   ```bash
   python manage.py runserver
   ```
3. Open a web browser and visit:
   ```
   http://localhost:8000
   ```

---

## 5. User Interface
- **Input Page:**
  - Allows users to enter text for encryption or decryption.
- **Output Display:**
  - Displays the encrypted or decrypted text clearly.

---

## 6. Tools for Video Recording
To create a video tutorial for the project, you can use one of the following tools:
1. **OBS Studio** (Free and open-source).
2. **Camtasia** (Professional-grade tool).
3. **Screencastify** (Browser extension for Chrome).

---

## Contact
If you have any questions or need support, feel free to reach out.
