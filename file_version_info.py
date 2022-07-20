import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version="1.0",
    company_name="TecWindow",
    file_description="With this program, you can search or browse any Wikipedia article. site: https://t.me/tecwindow",
    internal_name="WikiSearch",
    legal_copyright="© My TecWindow Company. All rights reserved.",
    original_filename="WikiSearch.exe",
    product_name="WikiSearch"
)
