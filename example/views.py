import os
import subprocess
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files.base import ContentFile


def home(request):
    return render(request, "example/home.html", {})


def visualize(request):
    if request.method == "POST":
        # Process the uploaded files
        banks_file = request.FILES.get("banksFile")
        transactions_file = request.FILES.get("transactionsFile")
         
        if banks_file and transactions_file:
            try:
                # Save the files temporarily using default_storage
                banks_file_path = default_storage.save(
                    banks_file.name, ContentFile(banks_file.read())
                )
                transactions_file_path = default_storage.save(
                    transactions_file.name, ContentFile(transactions_file.read())
                )
                banks_file_full_path = default_storage.path(banks_file_path)
                transactions_file_full_path = default_storage.path(
                    transactions_file_path
                )

                # Run the C++ program with the files as input
                exe_path = os.path.join(
                    settings.BASE_DIR, "example", "static", "ago.exe"
                )
                result = subprocess.run(
                    [exe_path, banks_file_full_path, transactions_file_full_path],
                    capture_output=True,
                    text=True,
                )

                # Check if the C++ program ran successfully
                if result.returncode == 0:
                    output = result.stdout
                else:
                    output = result.stderr

                # Return the output as JSON response
                return JsonResponse({"answer": output})

            finally:
                # Clean up the temporary files
                default_storage.delete(banks_file_path)
                default_storage.delete(transactions_file_path)
        else:
            return JsonResponse({"error": "Files are required"}, status=400)
    else:
        return render(request, "example/home.html")
