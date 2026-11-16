const { app } = require('@azure/functions');

app.http('conversorInternacional', {
    methods: ['POST'],
    authLevel: 'anonymous',

    handler: async (request, context) => {
        context.log('Iniciando conversão de moedas.');

        // 1. Ler o JSON recebido
        let dados;

        try {
            dados = await request.json();
        } catch {
            return {
                status: 400,
                jsonBody: { erro: 'O corpo deve conter um JSON válido.' }
            };
        }

        // 2. Validar o valor em reais
        if (
            !dados ||
            !Number.isFinite(dados.valorReais) ||
            dados.valorReais < 0
        ) {
            return {
                status: 400,
                jsonBody: {
                    erro: 'valorReais deve ser um número maior ou igual a zero.'
                }
            };
        }

        const valorReais = dados.valorReais;

        // Cotações demonstrativas, não consultadas no mercado
        const cotacaoDolar = dados.cotacaoDolar ?? 5.0;
        const cotacaoEuro = dados.cotacaoEuro ?? 6.25;

        // 3. Validar as cotações
        if (
            !Number.isFinite(cotacaoDolar) ||
            cotacaoDolar <= 0 ||
            !Number.isFinite(cotacaoEuro) ||
            cotacaoEuro <= 0
        ) {
            return {
                status: 400,
                jsonBody: {
                    erro: 'As cotações devem ser números maiores que zero.'
                }
            };
        }

        try {
            // 4. Calcular
            const valorDolar = valorReais / cotacaoDolar;
            const valorEuro = valorReais / cotacaoEuro;

            if (
                !Number.isFinite(valorDolar) ||
                !Number.isFinite(valorEuro)
            ) {
                return {
                    status: 400,
                    jsonBody: {
                        erro: 'Os valores informados excedem o limite de cálculo.'
                    }
                };
            }

            // 5. Retornar os resultados em JSON
            return {
                status: 200,
                jsonBody: {
                    provedor: 'Azure',
                    valorReais,
                    valorDolar: Number(valorDolar.toFixed(2)),
                    valorEuro: Number(valorEuro.toFixed(2)),
                    cotacaoDolar,
                    cotacaoEuro,
                    cotacaoSimulada: true
                }
            };
        } catch (error) {
            context.error('Falha na conversão:', error);

            return {
                status: 500,
                jsonBody: { erro: 'Erro interno ao realizar a conversão.' }
            };
        }
    }
});