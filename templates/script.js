$(document).ready(function() {
    $("#calculate-button").click(function() {
        // Get form data
        var formData = {
            gross: $("#gross").val(),
            health: $("#health").val(),
            contrib: $("#contrib").val()
        };

        // Send POST request to Flask server
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/payslip", // URL of your Flask endpoint
            data: formData,
            dataType: "json", // Expected response data type
            success: function(response) {
                console.log(data);
                console.log(FormData);
                console.log(response);
                // Display the response in the result div
                $("#result").html("Net Pay: " + response.payslip + "<br>" +
                                   "Payee: " + response.payee + "<br>" +
                                   "Health Insurance payment: " + response.health + "<br>" +
                                   "National Housing Fund: " + response.housing + "<br>" +
                                   "Pension: " + response.pension);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });
});
