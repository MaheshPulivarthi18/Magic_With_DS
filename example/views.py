import os
import subprocess
import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "example/home.html", {})


def visualize(request):
    if request.method == "POST":
        banks_file_path = request.POST.get("banksFilePath", "").strip().strip('"')
        transactions_file_path = (
            request.POST.get("transactionsFilePath", "").strip().strip('"')
        )

        logger.debug(f"Received banksFilePath: {banks_file_path}")
        logger.debug(f"Received transactionsFilePath: {transactions_file_path}")

        if banks_file_path and transactions_file_path:
            try:
                # Ensure the paths are valid
                if not os.path.exists(banks_file_path) or not os.path.exists(
                    transactions_file_path
                ):
                    logger.warning("One or both files do not exist.")
                    return JsonResponse(
                        {"error": "One or both files do not exist"}, status=400
                    )

                # Set the executable path
                exe_path = os.path.join(
                    settings.BASE_DIR, "example", "static", "ago.exe"
                )
                os.chmod(exe_path, 0o755)

                # Run the C++ program with the provided file paths as input
                result = subprocess.run(
                    [exe_path, banks_file_path, transactions_file_path],
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
            logger.warning(
                "Both banks file path and transactions file path are required."
            )
            return JsonResponse(
                {
                    "error": "Both banks file path and transactions file path are required"
                },
                status=400,
            )

    else:
        return render(request, "example/home.html")


def favicon(request):
    return HttpResponse(status=204)
