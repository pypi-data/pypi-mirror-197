from typing import Type
from numpy import nan
from .helper import timing

@timing
def ensure_dtypes(df:Type)-> Type:
    """
    Funcao feita para garantir que as colunas que são supostas 
    serem númericas realmente estarem em formato númerico. Tambem verifica se tem valores nulos.
    """
    df['user_phone'] = df.user_phone.str.replace('\D*','',regex = True).replace('',nan)
    df['original_user_id'] = df.original_user_id.replace('',nan)
    if df['user_phone'].isna().any():
        print('\033[93mAviso: Detectei nulos na coluna userphone! Formulando tratativa\033[0m')
        start_na = df['user_phone'].isna().sum()
        df['user_phone'] = df.groupby('original_user_id',group_keys = False)['user_phone'].apply(lambda x : x.bfill().ffill())
        end_na = df['user_phone'].isna().sum()
        print(f'\033[93m O número de nulos na coluna user_phone foi de {start_na} para {end_na}\033[0m')

    if df['original_user_id'].isna().any():
        print('\033[93mAviso: Detectei nulos na colunas original_user_id! Formulando tratativa!\033[0m')
        start_na = df['original_user_id'].isna().sum()
        df['original_user_id'] = df.groupby('user_phone',group_keys = False)['original_user_id'].apply(lambda x : x.bfill().ffill())
        end_na = df['original_user_id'].isna().sum()
        print(f'\033[93mO número de nulos na coluna original_user_id foi de {start_na} para {end_na}\033[0m')
    return df

@timing
def dtype_tracking(df:Type) -> Type:
    """
    Tratando os dtypes para que eles estejam bonitinhos,
    em relacao a memoria, utilizada evitando custos! Em layer.
    """
    dtypes= {
        'chatbot_id':str,
        'user_phone':str,
        'category':str,
        'action':str,
        'suffix':str,
        'original_user_id':str,
        'queued_date_service':'datetime64[ns]',
        'id':str,# Alterar no futuro
    }
    new_df = df.astype(dtype = dtypes)
    return new_df

@timing
def remove_test(df:Type) -> Type:
    """
    Funcao que remove users teste (testes joga fora)
    """
    testers = { 
                'Adriano': '11989999375',
                'Bruno': '13981074058', 
                'Maicon Veiga': '11969309352',
                'Jessica Varçal': '11970325152',
                'Ana Flávia Dumo': '11997842525', 
                'Sabrina Augusta': '11971565507', 
                'Salvo Menezes': '11980602111',
                'Sueli Maria': '11999171150', 
                'Leticia Dominique': '11984435186', 
                'Sueli Ferreira': '11941606552', 
                'Joana Sargo': '351910191617', 
                'Ingrid Lemos': '11987361937', 
                'Harrison Pompilha': '11982454209', 
                'Jefferson Andrade': '11986226831', 
                'Renan': '11943615412',
                'Ana Portillo': '11995879008',
                'Rafael Rodrigues': '11986705117', 
                'Andréia Lorenzoni': '11949855198',
                'Lucas Paixão': '11956075838',
                'Alexandre Pavaneli': '17997472596',
                'Murillo Nozue': '11994117676', 
                'Thiago Rasquino': '11981333149', 
                'Luis Henrique': '11986309778', 
                'Guilherme Garcia': '11984738427', 
                'Gabriel Brandao': '11940667922', 
                'Diego Coutino': '21981025516', 
                'Cintia Oliveira': '11997061023', 
                'Anderson Martins': '11974029844',
                'Alline': '11983842161', 
                'Vinicius Tirello': '34996473073', 
                'Bruna Minnicelli': '11991680459',
                'Guilherme Rapicham':'43999264449'
            }
    filt = df['user_phone'].isin(testers.values())
    if df.loc[filt].empty:
        print('\033[93mAviso: Nenhum teste foi encontrado!\033[0m')
        return df
    df = df.loc[~filt].reset_index(drop = True)
    return df

@timing
def steps(s:Type) -> Type:
    """
    Formula coluna steps de acordo com a coluna suffix
    s =  suffix series
    """
    unstepped_trackings = []
    st = []
    for i in s:
        if 'onbo' in i:
            if 'start' in i:
                st.append('1-Onboarding + Retorno')
            elif 'segment' in i:
                st.append('1.1-Onboarding escolha de bot')
            else:
                st.append(nan)
        elif 'product-selection' in i:
            st.append('2-Seleciona produto')
        elif 'product-availability' in i:
            if 'cpf-request' in i:
                st.append('3-Informa localizacao e cpf')
            elif 'cpf-validation' in i:
                st.append('3.1-CPF valido (V.2.0)')
            elif 'postalcode-request' in i:
                st.append('3.2-Obtencao de CEP')
            elif 'postalcode-validation options' in i:
                st.append('3.3-CEP valido (V.2.2)')
            elif 'postalcode-validation-true' in i:
                st.append('3.4-Passa endereco')
            elif 'health-api-address-validation' in i:
                st.append('3.5-Endereco valida (V.2.3)')
            elif 'address-confirmation' in i:
                st.append('3.6-Endereco resumido')
            elif 'health-api-residential-customer-contracts-validation' in i:
                st.append('3.7-Consulta de CPF na api de base(V.2.9)')
            elif 'client-validation' in i:
                st.append('3.8-Localizado na api de base (V.2.10)')
            elif 'product-availability-validation' in i:
                st.append('3.9-Produto e disponibilizado na regiao (V.2.12)')
            elif 'health-api-plan-availability-validation' in i:
                st.append('3.9.1-Consulta na api de catalogos(V.2.13)')
            elif 'plans-available-catalog-validation' in i:
                st.append('3.9.2-Plano disponivel no catalogo (V.2.14)')
            else:
                st.append(nan)
        elif 'plan-selection' in i:
            st.append('4-Escolhe plano (Todos produtos)')
        elif 'registration' in i:
            if 'full-name-request' in i:
                st.append('5-Realiza cadastro')
            elif 'name-validation' in i:
                st.append('5.1-Consulta nome valido (V.4.0)')
            elif 'email-request' in i:
                st.append('5.2-Requisicao de email')
            elif 'e-mail-validation' in i:
                st.append('5.3-Consulta email valido (V.4.1)')
            elif 'birth-date-request' in i:
                st.append('5.4-Idade do usuario')
            elif 'birth-date-validation' in i:
                st.append('5.5-Idade do usuario validacao (V.4.2)')
            elif 'birth-date-out-of-range-validation' in i:
                st.append('5.6-Idade do usuario elegibilidade (V.4.3)')
            elif 'identity-number-request' in i:
                st.append('5.7-Pedido de RG')
            elif 'identity-number-validation' in i:
                st.append('5.8-Pedido de RG (V.4.4)')
            elif 'mother-name-request' in i:
                st.append('5.9-Pedido de nome da mae')
            elif 'mother-name-validation' in i:
                st.append('5.9.1-Pedido de nome da mae validation (V.4.5)')
            elif 'additional-phone-number-confirmation' in i:
                st.append('5.9.2-Numero adicional')
            elif 'register-data-confirmation' in i:
                st.append('5.9.3-Confirmacao de data')
            elif 'address-complement-insert-confirmation' in i:
                st.append('6-Informa Complemento')
            elif 'address-complement-confirmation' in i:
                st.append('6.1-Complemento confirmado')
            else:
                st.append(nan)
        elif 'payment' in i:
            if 'invoice-sending-confirmation' in i:
                st.append('7-Metodo de pagamento')
            elif 'invoice-due-date-options' in i:
                st.append('7.1-Escolhe dia de vencimento')
            elif 'payment-method-confirmation-options' in i:
                st.append('7.2-Escolhe forma de pagamento')
            elif 'register-data-confirmation' in i:
                st.append('7.3-Confirma dados')
            else:
                st.append(nan)
        elif 'schedule start' in i:
            st.append('8-Agendamento de instalacao')
        elif 'checkout' in i:
            if 'order-details-confirmation' in i:
                st.append('9-Realiza pedido')
            elif 'order-validation' in i:
                st.append('9.1-Cascata de api (V.F.0)')
            elif 'order-placed userphone' in i:
                st.append('9.2-Finalizado')
            else:
                st.append(nan)
        elif 'error' in i:
            st.append('Horizontal-erros-gerais')
        elif 'human-handoff' in i:
            st.append('Horizontal-Transbordo')
        elif 'decision-tree' in i:
            st.append('Horizontal-Cascatas')
        elif 'feedback' in i:
            st.append('Horizantal-Feedback')
        else:
            unstepped_trackings.append(i)
            st.append(nan)
    if any([i is not nan for i in unstepped_trackings]):
        print('\033[93mAviso: Voce tem trackings sem steps! Para ver quais são verificar lista unstepped_trackings :)\033[0m')
    return st

@timing
def errors(s:Type) -> Type:
    """
    Formula coluna de erros
    """
    e = []
    for i in s:
        if 'error' in i:
            if 'unexpected-video' in i:
                e.append('Erro video')
            elif 'unexpected-image' in i:
                e.append('Erro imagem')
            elif 'unexpected-audio' in i:
                e.append('Erro audio')
            elif 'unexpected-file' in i:
                e.append('Erro arquivo')
            elif 'unexpected-cpf' in i:
                e.append('Erro persistente CPF')
            elif 'generic' in i:
                e.append('Erro generico')
            elif 'api' in i:
                e.append('Erro generico API')
            elif 'last-state-unidentified' in i:
                e.append('Erro estado inexistente')
            elif 'bob' in i:
                e.append('Erro Bob')
            else:
                e.append(nan)
        else:
            e.append(nan)
    if any([i is not nan for i in e]):
        print('\033[93mAviso: Tivemos erros no bot :(\033[0m')
    return e

# Migrar para outro lambda
def get_rid_of_undefined(df:Type) -> Type:
    """
    Ver com vini, capacidade extracao
    """
    pass

