// Formatadores de campo em tempo real
function formatarCNPJ(valor) {
    valor = valor.replace(/\D/g, '').substring(0, 14);
    if (valor.length > 8) {
        return valor.substring(0, 2) + '.' + valor.substring(2, 5) + '.' + 
               valor.substring(5, 8) + '/' + valor.substring(8, 12) + '-' + valor.substring(12, 14);
    } else if (valor.length > 5) {
        return valor.substring(0, 2) + '.' + valor.substring(2, 5) + '.' + valor.substring(5);
    } else if (valor.length > 2) {
        return valor.substring(0, 2) + '.' + valor.substring(2);
    }
    return valor;
}

function formatarTelefone(valor) {
    valor = valor.replace(/\D/g, '').substring(0, 11);
    if (valor.length === 11) {
        return '(' + valor.substring(0, 2) + ') ' + valor.substring(2, 7) + '-' + valor.substring(7, 11);
    } else if (valor.length === 10) {
        return '(' + valor.substring(0, 2) + ') ' + valor.substring(2, 6) + '-' + valor.substring(6, 10);
    } else if (valor.length > 2) {
        return '(' + valor.substring(0, 2) + ') ' + valor.substring(2);
    }
    return valor;
}

function formatarCEP(valor) {
    valor = valor.replace(/\D/g, '').substring(0, 8);
    if (valor.length === 8) {
        return valor.substring(0, 5) + '-' + valor.substring(5, 8);
    }
    return valor;
}

// Aplicar formatadores aos campos
document.addEventListener('DOMContentLoaded', function() {
    // Campo CNPJ
    const cnpjInput = document.querySelector('[name="cnpj"]');
    if (cnpjInput) {
        cnpjInput.addEventListener('input', function() {
            this.value = formatarCNPJ(this.value);
        });
    }

    // Campo Telefone
    const telefoneInput = document.querySelector('[name="telefone"]');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function() {
            this.value = formatarTelefone(this.value);
        });
    }

    // Campo CEP
    const cepInput = document.querySelector('[name="cep"]');
    if (cepInput) {
        cepInput.addEventListener('input', function() {
            this.value = formatarCEP(this.value);
        });
    }

    // Buscar cidade e estado automaticamente quando CEP é preenchido
    if (cepInput) {
        cepInput.addEventListener('blur', function() {
            if (this.value.length === 9) { // Formato XXXXX-XXX
                const cep = this.value.replace(/\D/g, '');
                buscarEnderecoPorCEP(cep);
            }
        });
    }
});

// Função para buscar endereço via ViaCEP API
function buscarEnderecoPorCEP(cep) {
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (!data.erro) {
                // Preencher campos automaticamente
                const ruaInput = document.querySelector('[name="rua"]');
                const bairroInput = document.querySelector('[name="bairro"]');
                const cidadeInput = document.querySelector('[name="cidade"]');
                const estadoInput = document.querySelector('[name="estado"]');

                if (ruaInput && data.logradouro) {
                    ruaInput.value = data.logradouro;
                }
                if (bairroInput && data.bairro) {
                    bairroInput.value = data.bairro;
                }
                if (cidadeInput && data.localidade) {
                    cidadeInput.value = data.localidade;
                }
                if (estadoInput && data.uf) {
                    estadoInput.value = data.uf;
                }
            }
        })
        .catch(error => {
            console.log('Não foi possível buscar o CEP:', error);
        });
}
