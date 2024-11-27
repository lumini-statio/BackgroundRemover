import os
import argparse
from datetime import datetime
from rembg import remove


class BackgroundRemover:
    def __init__(self, input_folder='input', output_folder='output'):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_images(self):
        today = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

        proccessed_folder = os.path.join(self.output_folder, today)
        os.makedirs(proccessed_folder, exist_ok=True)

        for filename in os.listdir(self.input_folder):
            if filename.endswith(('.png','jpg','jpeg')):
                input_path = os.path.join(self.input_folder, filename)
                output_path = os.path.join(proccessed_folder, filename)
                self._remove_bg(input_path, output_path)
                self._move_originals(input_path, proccessed_folder)

    def _remove_bg(self, input_path, output_path):
        with open(input_path, 'rb') as inp, open(output_path, 'wb') as otp:
            bg_output = remove(inp.read())
            otp.write(bg_output)

    def _move_originals(self, input_path, dest_path):
        original_folder = os.path.join(dest_path, 'originals')
        os.makedirs(original_folder, exist_ok=True)

        filename = os.path.basename(input_path)
        new_path = os.path.join(original_folder, filename)
        os.rename(input_path, new_path)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Script para remover fondo de imágenes")
    subparsers = parser.add_subparsers(dest='command', help='Subcomandos')

    parser_create = subparsers.add_parser('create_folders', help='Create folders for input and output')
    parser_process = subparsers.add_parser('process_images', help='Process images and remove the background')

    args = parser.parse_args() 

    if not args.command:
        parser.print_help() 
        
    elif args.command == 'create_folders': 
        os.makedirs('input', exist_ok=True) 
        os.makedirs('output', exist_ok=True) 
        print("Folders 'input' and 'output' where created succesfuly") 

    elif args.command == 'process_images': 
        remover = BackgroundRemover()
        remover.process_images()