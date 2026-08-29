// Este ficheiro corre em TODAS as paginas (porque vamos carrega-lo no base.html)

// 1) Fazer as mensagens de sucesso/erro desaparecerem sozinhas depois de 4 segundos
document.addEventListener('DOMContentLoaded', function () {
    const mensagens = document.querySelectorAll('.alert');
    mensagens.forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(function () { msg.remove(); }, 500);
        }, 4000); // 4000 milissegundos = 4 segundos
    });
});

// 2) Pedir confirmacao antes de qualquer botao/link marcado com data-confirmar
document.addEventListener('click', function (evento) {
    const alvo = evento.target.closest('[data-confirmar]');
    if (!alvo) return; // clique nao foi num elemento com essa marca, ignora

    const mensagem = alvo.getAttribute('data-confirmar');
    if (!confirm(mensagem)) {
        evento.preventDefault(); // cancela o clique se o utilizador disser "Cancelar"
    }
});
