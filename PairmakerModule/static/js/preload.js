window.addEventListener("load", function (event) {
    var contentDiv = document.querySelector('#content');
    var preloadDiv = document.querySelector('#preload');
    contentDiv.setAttribute('class', 'isVisible');
    preloadDiv.setAttribute('class', 'isHidden');
});

document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
});