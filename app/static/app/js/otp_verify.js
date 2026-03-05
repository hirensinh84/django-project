const otpinput=document.querySelectorAll('.otp-input');

otpinput.forEach((input) => {
    
    input.addEventListener('keypress', function(e) {
        if (e.which < 48 || e.which > 57) {
            e.preventDefault();
        }
    });

    input.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
    });
});