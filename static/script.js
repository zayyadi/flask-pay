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
            url: "http://147.182.228.231:5000/payslip", // URL of your Flask endpoint
            data: formData,
            dataType: "json", // Expected response data type
            success: function(response) {
                console.log(response);
                // Display the response in the result div
                $("#result").html("Monthly Payslip: " + response.payslip + "<br>" +
                                   "Payee: " + response.payee + "<br>" +
                                   "Consolidated Relief: " + response.cons + "<br>" +
                                   "Taxable Income: " + response.taxable + "<br>" +
                                   "Pension: " + response.pension);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });
});
