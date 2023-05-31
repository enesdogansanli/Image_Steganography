import cv2
import gradio
import numpy as np
import pandas as pd

import steganography


def encrypt_image(image_path,data,choose_rgb,row_shift,column_shift):
    print(image_path,data,choose_rgb,row_shift,column_shift)
    image_enc = cv2.imread(image_path)
    stego_image = steganography.steganography_endoce_image(image_enc,data,int(choose_rgb),int(row_shift),int(column_shift))
    cv2.imshow("Steganography image",stego_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # if public_exponent == "":
    #     public_exponent = 65537

    # try:
    #     public_exponent = float(public_exponent)
    # except ValueError:
    #     raise gradio.Error("Public exponent must be integer type")

    # if (public_exponent != int(public_exponent)):
    #     raise gradio.Error("Public exponent must be integer type")

    # if (rsa_gs.RSA_GS.is_prime(public_exponent) == False):
    #     raise gradio.Error("Public exponent must be prime number")

    # if (public_exponent < 65537):
    #     raise gradio.Error("Public exponent must be graeter than 65537")

    # try:
    #     modulus = float(modulus)
    # except ValueError:
    #     raise gradio.Error("Modulus must be integer type")

    # if (modulus != int(modulus)):
    #     raise gradio.Error("Modulus must be integer type")

    # try:
    #     shift = float(shift)
    # except ValueError:
    #     raise gradio.Error("Shift count must be integer type")

    # if (shift != int(shift)):
    #     raise gradio.Error("Shift count must be integer type")

    # return rsa_gs.RSA_GS.encrypt((int(public_exponent), int(modulus)),
    #                              int(shift), plaintext)


def decrypt_text(image_path,choose_rgb,row_shift,column_shift):
    image_for_dec = cv2.imread(image_path)
    print(image_for_dec)
    find_text = steganography.steganography_decode_image(image_for_dec,int(choose_rgb),int(row_shift),int(column_shift))
    print(find_text)
    return find_text

    # try:
    #     private_exponent = float(private_exponent)
    # except ValueError:
    #     raise gradio.Error("Private exponent must be integer type")

    # if (private_exponent != int(private_exponent)):
    #     raise gradio.Error("Private exponent must be integer type")

    # try:
    #     modulus = float(modulus)
    # except ValueError:
    #     raise gradio.Error("Modulus must be integer type")

    # if (modulus != int(modulus)):
    #     raise gradio.Error("Modulus must be integer type")

    # try:
    #     shift = float(shift)
    # except ValueError:
    #     raise gradio.Error("Shift count must be integer type")

    # if (shift != int(shift)):
    #     raise gradio.Error("Shift count must be integer type")

    # return rsa_gs.RSA_GS.decrypt((int(private_exponent), int(modulus)),
    #                              ciphertext, int(shift))

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

            # with gradio.Column():
                # gradio.Image(image_path_for_encryption)

        encrypt_button = gradio.Button("Encrypt")

    with gradio.Tab("Decryption"):
        with gradio.Row():
            with gradio.Column():
                image_path_for_decryption = gradio.Textbox(
                    label="Image path",
                    placeholder="Enter the image path...")
                choose_rgb_for_decryption = gradio.Number(
                    label="Choose rgb")
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
                         outputs=[])

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
