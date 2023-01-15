<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>TheDarkPortal</title>
</head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js" integrity="sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" integrity="sha384-+sLIOodYLS7CIrQpBjl+C7nPvqq+FbNUBDunl/OZv93DB7Ln/533i8e/mZXLi/P+" crossorigin="anonymous"></script>
<body>
<div
        style="background-image: url('imgs/portal.jpg');height: 100vh;background-repeat: no-repeat;background-size:cover">

    <div class="d-flex justify-content-center align-items-center" style="height:100vh;">
        <main role="main" class="inner cover">
            <h1 class="cover-heading text-white">Voices from the other side of The Dark Portal:</h1>
            <p class="lead text-white" id="voice"><strong>...</strong></p>
        </main>
    </div>
</div>
<script>

 $(document).ready(function () {
     $.ajax({
         url: "7he_d4rk_p0rt4l",
         type: "GET",
         success: function (data) {
             $("#voice").html(data);
         }
     })
 });

</script>
</body>
</html>
