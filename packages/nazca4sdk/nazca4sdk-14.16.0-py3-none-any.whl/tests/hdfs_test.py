"""Testing nazca4sdk """

from nazca4sdk.datahandling.file.file_storage import FileStorage

# sdk = SDK()
# print(sdk.modules)

fs = FileStorage(True)
file = fs.download_file("/siemka.txt", "./siemka.txt")
# fs.send_file('/Sodomita.txt', "./Korek.txt")
print("OK")
