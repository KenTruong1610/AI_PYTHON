import tkinter as tk
from tkinter import filedialog
import os
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes  



# Chuyển đổi từ Hexadecimal sang binary
def hex_to_bin(hex_string):
    decimal_representation = int(hex_string, 16)
    binary_representation = bin(decimal_representation)[2:]  # Remove the '0b' prefix
    return binary_representation.zfill(64)


# Chuyển đổi từ binary sang hexadecimal
def bin_to_hex(binary_string):
    mapping = {"0000": '0',
		"0001": '1',
		"0010": '2',
		"0011": '3',
		"0100": '4',
		"0101": '5',
		"0110": '6',
		"0111": '7',
		"1000": '8',
		"1001": '9',
		"1010": 'A',
		"1011": 'B',
		"1100": 'C',
		"1101": 'D',
		"1110": 'E',
		"1111": 'F'}
    
    hex = ""
    for i in range(0, len(binary_string), 4):
        ch = ""
        ch = ch + binary_string[i]
        ch = ch + binary_string[i + 1]
        ch = ch + binary_string[i + 2]
        ch = ch + binary_string[i + 3]
        hex = hex + mapping[ch]
    
    return hex

# Chuyển đổi từ Binary sang decimal
def bin_to_dec(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


# Chuyển đổi từ Decimal sang Binary
def dec_to_bin(num):
    res = bin(num).replace("0b", "")
    if len(res) % 4 != 0:
        div = len(res) / 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = "0" + res
    return res


# Bảng mở rộng e
exp_table = [32, 1, 2, 3, 4, 5, 4, 5,
            6, 7, 8, 9, 8, 9, 10, 11,
            12, 13, 12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21, 20, 21,
            22, 23, 24, 25, 24, 25, 26, 27,
            28, 29, 28, 29, 30, 31, 32, 1]

# Bảng P
p_table = [16, 7, 20, 21,
		29, 12, 28, 17,
		1, 15, 23, 26,
		5, 18, 31, 10,
		2, 8, 24, 14,
		32, 27, 3, 9,
		19, 13, 30, 6,
		22, 11, 4, 25]

# S-box
sbox = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]

# Bảng IP-1
IP_1 = [40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
			34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25]


# Hàm hoán vị
def permute(key, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + key[arr[i] - 1]
    return permutation


# Tính xor
def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans


# Hàm dịch trái
def RotleftShift(key, shift_num):
    s = ""
    for i in range(shift_num):
        for j in range(1, len(key)):
            s = s + key[j]
        s = s + key[0]
        key = s
        s = ""
    return key


# Tính hoán vị IP
def IPM(plain_text):
    # Bảng IP
    IP =    [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

    # chuyển key từ dạng hex sang binary
    plain_text = hex_to_bin(plain_text)

    # Hoán vị PC1
    plain_text = permute(plain_text, IP, 64)

    return plain_text


# Tính hoán vị PC-1
def PC1K(key):
    # Bảng PC1
    pc1 = [57, 49, 41, 33, 25, 17, 9,
		1, 58, 50, 42, 34, 26, 18,
		10, 2, 59, 51, 43, 35, 27,
		19, 11, 3, 60, 52, 44, 36,
		63, 55, 47, 39, 31, 23, 15,
		7, 62, 54, 46, 38, 30, 22,
		14, 6, 61, 53, 45, 37, 29,
		21, 13, 5, 28, 20, 12, 4]

    # chuyển key từ dạng hex sang binary
    key = hex_to_bin(key)

    # Hoán vị PC1
    key = permute(key, pc1, 56)

    return key


# Tính hoán vị PC-2
def PC2(key):
    # Bảng số lượng dịch trái
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # Bảng PC2
    pc2 = [14, 17, 11, 24, 1, 5,
			3, 28, 15, 6, 21, 10,
			23, 19, 12, 4, 26, 8,
			16, 7, 27, 20, 13, 2,
			41, 52, 31, 37, 47, 55,
			30, 40, 51, 45, 33, 48,
			44, 49, 39, 56, 34, 53,
			46, 42, 50, 36, 29, 32]

    # Chia key thành 2 nửa trái và phải
    left_key = PC1K(key)[0:28]
    right_key = PC1K(key)[28:56]

    ki = []  


    for i in range(0, 16):
        # Dịch trái cho left key
        left_key = RotleftShift(left_key, shift_table[i])
        # Dịch trái cho right key
        right_key = RotleftShift(right_key, shift_table[i])

        # nối key
        combine_key = left_key + right_key

        # Hoán vị PC2
        round_key = permute(combine_key, pc2, 48)

        ki.append(round_key)

    return  ki


def encrypt(plain_text, ki):
    # Hoán vị IP
    plain_text = IPM(plain_text)

    left_text = plain_text[0:32]
    right_text = plain_text[32:64]

    # lặp 16 vòng
    for i in range(0, 16):
        # Mở rộng E bên phải
        right_expanded = permute(right_text, exp_table, 48)
        
        # Thực hiện xor giữa mở rộng E và ki 
        xor_x = xor(right_expanded, ki[i])
        
        # Thế S-box
        sbox_str = ""
        for j in range(0, 8):
            row = bin_to_dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin_to_dec(
                int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec_to_bin(val)

        # Hoán vị P
        sbox_str = permute(sbox_str, p_table, 32)
        
        # Xor giữa nửa trái và sbox
        result = xor(left_text, sbox_str)
        left_text = result
        
        if i != 15:
            left_text, right_text = right_text, left_text

    
    combine = left_text + right_text
    # Hoán vị IP-1
    cipher_text = permute(combine, IP_1, 64)
    # Chuyển từ binary sang hex
    cipher_text = bin_to_hex(cipher_text)
    return cipher_text

# GUI
class FileEncryptorDecryptor:
    def __init__(self, master):
        self.master = master
        self.master.title("CHƯƠNG TRÌNH MÃ HÓA HỢP ĐỒNG DES")
        
        

        self.file_path_label = tk.Label(self.master, text="Hợp đồng:")
        self.file_path_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.file_path_entry = tk.Entry(self.master, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(self.master, text="Chọn File", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.key_label = tk.Label(self.master, text="Key:")
        self.key_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.key_entry = tk.Entry(self.master, width=50)
        self.key_entry.grid(row=1, column=1, padx=5, pady=5)

        self.generate_key_button = tk.Button(self.master, text="Tạo key", command=self.generate_key)
        self.generate_key_button.grid(row=1, column=2, padx=5, pady=5)

        self.encrypt_button = tk.Button(self.master, text="Mã hóa", command=self.encrypt_file)
        self.encrypt_button.place(x = 170, y = 90)

        self.decrypt_button = tk.Button(self.master, text="Giải mã", command=self.decrypt_file)
        self.decrypt_button.place(x = 270, y = 90)

        self.file_description_label = tk.Label(self.master, text="Lưu ý: chương trình chỉ hỗ trợ định dạng file: .txt, .doc, .docx, .xlxs, .pdf, .jpg, .png\n ")
        self.file_description_label.place(x = 30, y = 140)

    def browse_file(self):
        allowed_file_types = [
        ("PDF files", "*.pdf"),
        ("Word documents", "*.doc;*.docx"),
        ("Excel files", "*.xlsx"),
        ("Image files", "*.jpg;*.png"),
        ("Text files", "*.txt"),
        ("All files", "*.*")
    ]
        
        file_path = filedialog.askopenfilename(filetypes=allowed_file_types)
        
        if file_path:
            file_extension = file_path.lower().split('.')[-1]
            
            # Check if the file extension is allowed
            allowed_extensions = [ext.lower().lstrip('*.') for _, patterns in allowed_file_types for ext in patterns.split(";")]
            if file_extension not in allowed_extensions:
                tk.messagebox.showerror("Invalid File Type", "Định dạng file không hợp lệ.")
                return
            
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def generate_key(self):
        key = get_random_bytes(8)
        
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, key.hex())
        
        

    def is_valid_key(self, key):
        try:
            bytes.fromhex(key)
            return len(bytes.fromhex(key)) == 8
        except ValueError:
            return False

    def pad_data(self, data):
        block_size = DES.block_size
        return data + (block_size - len(data) % block_size) * b"\0"

    def unpad_data(self, data):
        # Find the index of the last non-null byte
        last_non_null_index = len(data) - 1
        while last_non_null_index >= 0 and data[last_non_null_index] == 0:
            last_non_null_index -= 1

        # Return the data up to the last non-null byte
        return data[:last_non_null_index + 1]


    def encrypt_file(self):
        file_path = self.file_path_entry.get()
        key = self.key_entry.get()

        if not file_path:
            tk.messagebox.showwarning("WARNING", "Vui lòng chọn File trước khi thực hiện!")
            return

        if not key:
            tk.messagebox.showwarning("WARNING", "Vui lòng tạo key trước khi thực hiện!")
            return
        
        if file_path and key:
            if self.is_valid_key(key):
                key = bytes.fromhex(key)
                
                with open(file_path, "rb") as file:
                    data = file.read()

                cipher = DES.new(key, DES.MODE_ECB)
                encrypted_data = cipher.encrypt(self.pad_data(data))
                
                # Determine the output file path
                output_file_path = file_path.replace(".", "_encrypted.")
                
                with open(output_file_path, "wb") as encrypted_file:
                    encrypted_file.write(encrypted_data)
                
                tk.messagebox.showinfo("Encryption", f"File đã được mã hóa thành công và được lưu với tên {output_file_path}")
            else:
                tk.messagebox.showerror("Invalid Key", "Key không hợp lệ. Vui lòng kiểm tra lại!")
                
                #save_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted Files", "*.enc"), ("All Files", "*.*")])


    def decrypt_file(self):
        file_path = self.file_path_entry.get()
        key = self.key_entry.get()
        
        if not file_path:
            tk.messagebox.showwarning("WARNING", "Vui lòng chọn File trước khi thực hiện!")
            return

        if not key:
            tk.messagebox.showwarning("WARNING", "Vui lòng tạo key trước khi thực hiện!")

        
        
        if file_path and key:
            if self.is_valid_key(key):
                key = bytes.fromhex(key)
                
                if '_encrypted.' not in os.path.basename(file_path):
                    decrypted_file_path = file_path.replace(".", "_decrypted.")
                    user_response = tk.messagebox.askquestion("Continue", "File không có định dạng _encrypted. Bạn có muốn tiếp tục giải mã không?")
                    if user_response != 'yes':
                        return
                else: 
                    decrypted_file_path = file_path.replace("_encrypted.", "_decrypted.")
                
                try:
                    with open(file_path, "rb") as file:
                        encrypted_data = file.read()

                    cipher = DES.new(key, DES.MODE_CBC)
                    decrypted_data = cipher.decrypt(self.unpad_data(encrypted_data))

                    with open(decrypted_file_path, "wb") as decrypted_file:
                        decrypted_file.write(decrypted_data)
                    
                    tk.messagebox.showinfo("Decryption", f"File đã được giải mã thành công và được lưu với tên {os.path.basename(decrypted_file_path)}")
                except Exception as e:
                    tk.messagebox.showerror("Decryption Error", f"Giải mã không thành công. Vui lòng kiểm tra lại file!")
            else:
                tk.messagebox.showwarning("Invalid Key", "Key không hợp lệ. Vui lòng kiểm tra lại!")

def main():
    root = tk.Tk()
    root.geometry("500x200")
    app = FileEncryptorDecryptor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
