import cv2
import gradio
import numpy as np
import pandas as pd

import steganography


def encrypt_image(image_path,data,choose_rgb,row_shift,column_shift):
    image_enc = cv2.imread(image_path)
    stego_image = steganography.steganography_endoce_image(image_enc,data,int(choose_rgb),int(row_shift),int(column_shift))
    # cv2.imshow("Steganography image",stego_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    new_stego_image = cv2.cvtColor(stego_image, cv2.COLOR_BGR2RGB)
    return new_stego_image

def decrypt_text(image_path,choose_rgb,row_shift,column_shift):
    image_for_dec = cv2.imread(image_path)
    find_text = steganography.steganography_decode_image(image_for_dec,int(choose_rgb),int(row_shift),int(column_shift))
    return find_text

with gradio.Blocks() as demo:
    with gradio.Tab("Encryption"):
        with gradio.Row():
            with gradio.Column():
                image_path_for_encryption = gradio.Textbox(
                    label="Image path",
                    placeholder=
                    "Enter the image path")
                data_for_encryption = gradio.Textbox(
                    label="Data",
                    placeholder="Enter the data ...")
                choose_rgb_for_encryption = gradio.Number(
                    label="Choose RGB")
                # Plaintext: Text that is not computationally tagged, specially formatted, or written in code.
                row_shift_for_encryption = gradio.Number(
                    label="Row shift")
                column_shift_for_encryption = gradio.Number(
                    label="Column shift")
            with gradio.Column():
                stego_image_for_encryption = gradio.Image(
                    label="Steganography image",
                    shape=(1080, 1920, 3),
                    image_mode="RGB")

        encrypt_button = gradio.Button("Encrypt")

    with gradio.Tab("Decryption"):
        with gradio.Row():
            with gradio.Column():
                image_path_for_decryption = gradio.Textbox(
                    label="Image path",
                    placeholder="Enter the image path...")
                choose_rgb_for_decryption = gradio.Number(
                    label="Choose RGB")
                # Ciphertext: Encrypted text transformed from plaintext using an encryption algorithm.
                row_shift_for_decryption = gradio.Number(
                    label="Row shift ")
                column_shift_for_decryption = gradio.Number(
                    label="Column shift")

            with gradio.Column():
                    text_from_image = gradio.Textbox(
                    label="Text from image",
                    placeholder="The result will be here after decryption...")

        decrypt_button = gradio.Button("Decrypt")

    encrypt_button.click(encrypt_image,
                         inputs=[
                             image_path_for_encryption,
                             data_for_encryption,
                             choose_rgb_for_encryption,
                             row_shift_for_encryption,
                             column_shift_for_encryption
                         ],
                         outputs=[stego_image_for_encryption])

    decrypt_button.click(decrypt_text,
                         inputs=[
                             image_path_for_decryption,
                             choose_rgb_for_decryption,
                             row_shift_for_decryption,
                             column_shift_for_decryption
                         ],
                         outputs=[
                             text_from_image
                         ])

# TODO: Uncomment demo.launch(share=True)
# demo.launch(share=True)
# server_port=8080
demo.launch()
