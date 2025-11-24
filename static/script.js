document.addEventListener("DOMContentLoaded", function() {
    console.log("Ahoy! O Quiz está pronto.");

    // Seleciona todos os inputs de opção (radio buttons) dentro do quiz
    // O seletor procura inputs com o name="resposta"
    const quizOptions = document.querySelectorAll('input[name="resposta"]');

    quizOptions.forEach(option => {
        // Adiciona um "ouvinte" para quando a opção mudar (for clicada)
        option.addEventListener('change', function() {
            // Encontra o formulário pai desse input
            const form = this.closest('form');
            
            // Submete o formulário automaticamente
            if (form) {
                // Pequeno atraso visual opcional (remova o setTimeout se quiser instantâneo absoluto)
                // Aqui está configurado para 200ms apenas para ver o clique
                setTimeout(() => {
                    form.submit();
                }, 150);
            }
        });
    });
});