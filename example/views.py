import os
import subprocess
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "example/home.html", {})


def visualize(request):
    if request.method == "POST":
        # Process the uploaded files
        banks_file = request.FILES.get("banksFile")
        transactions_file = request.FILES.get("transactionsFile")

        if banks_file and transactions_file:
            try:
                # Define the paths to the static files
                banks_file_static_path = os.path.join(
                    settings.BASE_DIR, "example", "static", "banksFile.txt"
                )
                transactions_file_static_path = os.path.join(
                    settings.BASE_DIR, "example", "static", "transactionsFile.txt"
                )

                # Write the uploaded content to the static files
                with open(banks_file_static_path, "wb") as f:
                    for chunk in banks_file.chunks():
                        f.write(chunk)
                with open(transactions_file_static_path, "wb") as f:
                    for chunk in transactions_file.chunks():
                        f.write(chunk)

                # Construct the path to the executable
                exe_path = os.path.join(
                    settings.BASE_DIR, "example", "static", "ago.exe"
                )

                # Run the C++ program with the static files as input
                result = subprocess.run(
                    [exe_path, banks_file_static_path, transactions_file_static_path],
                    capture_output=True,
                    text=True,
                    shell=True,
                )

                # Check if the C++ program ran successfully
                if result.returncode == 0:
                    output = result.stdout
                else:
                    output = result.stderr

                return JsonResponse({"answer": output})

            except Exception as e:
                logger.error(f"Error processing files: {e}")
                return JsonResponse({"error": "Internal server error"}, status=500)

        else:
            return JsonResponse({"error": "Files are required"}, status=400)
    else:
        return render(request, "example/home.html")
