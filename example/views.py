import os
import subprocess
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "example/home.html", {})


def visualize(request):
    if request.method == "POST":
        # Process the uploaded files
        banks_file = request.FILES.get("banksFile")
        transactions_file = request.FILES.get("transactionsFile")
        banks_file_tmp_path = None  # Initialize the variable here

        if banks_file and transactions_file:
            try:
                # Define the paths to the temporary files in %TEMP%
                banks_file_tmp_path = os.path.join(os.environ["TEMP"], "banksFile.txt")
                transactions_file_tmp_path = os.path.join(
                    os.environ["TEMP"], "transactionsFile.txt"
                )

                # Write the uploaded content to the temporary files
                with open(banks_file_tmp_path, "wb") as f:
                    for chunk in banks_file.chunks():
                        f.write(chunk)
                with open(transactions_file_tmp_path, "wb") as f:
                    for chunk in transactions_file.chunks():
                        f.write(chunk)

                # Construct the path to the executable
                exe_path = os.path.join(
                    settings.BASE_DIR, "example", "static", "ago.exe"
                )

                # Run the C++ program with the temporary files as input
                result = subprocess.run(
                    [exe_path, banks_file_tmp_path, transactions_file_tmp_path],
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

            finally:
                # Clean up the temporary files
                if banks_file_tmp_path and os.path.exists(banks_file_tmp_path):
                    os.remove(banks_file_tmp_path)
                if os.path.exists(transactions_file_tmp_path):
                    os.remove(transactions_file_tmp_path)
        else:
            return JsonResponse({"error": "Files are required"}, status=400)
    else:
        return render(request, "example/home.html")
