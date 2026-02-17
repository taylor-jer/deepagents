import pypandoc, sys
import os

def convert_md_to_docx(source_file, output_file):
    # Check if the source file exists
    if not os.path.exists(source_file):
        print(f"Error: {source_file} not found.")
        return

    try:
        # Download pandoc if it's not found on the system
        # pypandoc.ensure_pandoc_installed(show_progress=True)
        
        # Convert markdown to docx
        output = pypandoc.convert_file(source_file, 'docx', outputfile=output_file)
        
        if output == "":
            print(f"Success! Created: {output_file}")
            
    except RuntimeError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Settings
    input_md = sys.argv[1]
    output_docx = sys.argv[2]
    
    convert_md_to_docx(input_md, output_docx)
