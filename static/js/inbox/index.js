window.addEventListener('load', function () {
    $(document).on('click', '.image', function () {
        const letterContainer = $(this).data('letter-id');
        $(`#letterOutput${letterContainer}`).toggle();
        const token = localStorage.getItem('token');
        console.log(letterContainer);
        postUserReadMessageId(letterContainer);
    });

    function postUserReadMessageId(id) {
        $.ajax({
            type: 'POST',
            url: '/receive/msgRead',
            contentType: 'application/json',
            data: JSON.stringify({ m_id: id }),
            success: function (response) {
                console.log(response);
                window.location.reload();
            },
            error(e) {
                alert(e);
                window.location.reload();
            },
        });
    }

    const outBtn = document.getElementById('outBtn');
    outBtn.addEventListener('click', function () {
        window.location.href = '/authChk';
    });
});
