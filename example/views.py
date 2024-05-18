# example/views.py
import os
import subprocess
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, "example/home.html", {})


def visualize(request):
    if request.method == "POST":
        # Process the uploaded files
        banks_file = request.FILES.get("banksFile")
        transactions_file = request.FILES.get("transactionsFile")

        if banks_file and transactions_file:
            # Save the files temporarily
            fs = FileSystemStorage()
            banks_file_path = fs.save(banks_file.name, banks_file)
            transactions_file_path = fs.save(transactions_file.name, transactions_file)
            banks_file_full_path = fs.path(banks_file_path)
            transactions_file_full_path = fs.path(transactions_file_path)

            try:
                # Run the C++ program with the files as input
                exe_path = os.path.join(settings.BASE_DIR, 'static', 'executables', 'ago.exe')

# Run the subprocess with the dynamically constructed path
                result = subprocess.run(
                [
                    exe_path,
                    banks_file_full_path,
                    transactions_file_full_path,
                ],
                    capture_output=True,
                    text=True,
                    shell=True,
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
                os.remove(banks_file_full_path)
                os.remove(transactions_file_full_path)
        else:
            return JsonResponse({"error": "Files are required"}, status=400)
    else:
        return render(request, "example/home.html")
