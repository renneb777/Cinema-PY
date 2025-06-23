from kivy.app import App # type: ignore # type: ignore
from kivy.uix.boxlayout import BoxLayout # type: ignore
from kivy.uix.button import Button # type: ignore
from kivy.uix.label import Label # type: ignore
from kivy.uix.textinput import TextInput # type: ignore
from kivy.uix.carousel import Carousel # type: ignore
from kivy.uix.image import AsyncImage # type: ignore
from kivy.uix.scrollview import ScrollView # type: ignore
from kivy.uix.popup import Popup # type: ignore

class Filme:
    def __init__(self, titulo, diretor, genero, ano_lancamento):
        self.titulo = titulo
        self.diretor = diretor
        self.genero = genero
        self.ano_lancamento = ano_lancamento

class No:
    def __init__(self, filme):
        self.filme = filme
        self.proxNo = None

class ListaFilmes:
    def __init__(self):
        self.fim = None
        self.quant = 0

    def esta_vazia(self):
        return self.fim is None

    def insere_lista_vazia(self, novo_filme):
        novo_no = No(novo_filme)
        novo_no.proxNo = novo_no
        self.fim = novo_no
        self.quant += 1

    def insere_no_frente(self, novo_filme):
        novo_no = No(novo_filme)
        if self.fim is None:
            self.insere_lista_vazia(novo_filme)
            return
        novo_no.proxNo = self.fim.proxNo
        self.fim.proxNo = novo_no
        self.quant += 1

    def insere_no_fim(self, novo_filme):
        novo_no = No(novo_filme)
        if self.fim is None:
            self.insere_lista_vazia(novo_filme)
            return
        novo_no.proxNo = self.fim.proxNo
        self.fim.proxNo = novo_no
        self.fim = novo_no
        self.quant += 1

    def remove_do_inicio(self):
        if self.fim is None:
            return
        if self.fim.proxNo == self.fim:
            self.fim = None
        else:
            self.fim.proxNo = self.fim.proxNo.proxNo
        self.quant -= 1

    def exibe_lista(self):
        if self.fim is None:
            return "Lista de filmes vazia!"
        atual = self.fim.proxNo
        lista_filmes = []
        for _ in range(self.quant):
            lista_filmes.append(atual.filme)
            atual = atual.proxNo
        return lista_filmes
    
class MyTextInput(TextInput):
    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.bind(focus=self.on_focus_change)

    def on_focus_change(self, instance, value):
        if value:
            self.font_size = '30sp'
        else:
            self.font_size = '20sp'

class MultilistaFilmes:
    def __init__(self, num_listas):
        self.listas = [ListaFilmes() for _ in range(num_listas)]

    def insere_na_lista(self, indice_lista, filme):
        if 0 <= indice_lista < len(self.listas):
            self.listas[indice_lista].insere_no_frente(filme)
            return True
        return False

    def remove_da_lista(self, indice_lista):
        if 0 <= indice_lista < len(self.listas):
            self.listas[indice_lista].remove_do_inicio()
            return True
        return False

    def exibe_lista(self, indice_lista):
        if 0 <= indice_lista < len(self.listas):
            return self.listas[indice_lista].exibe_lista()
        return "Lista de filmes inválida!"

class FilmeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multilista_filmes = MultilistaFilmes(num_listas=3)  

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Carousel de imagens
        carousel_layout = self.create_carousel()
        layout.add_widget(carousel_layout)

        # Caixa de mensagem
        self.message_box = Label(text='', size_hint=(1, 0.3))
        layout.add_widget(self.message_box)

        # Widgets para entrada de dados
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.11))
        
        self.titulo_input = MyTextInput(hint_text='Título do filme', font_size='20sp', size_hint=(0.15, 1))
        self.diretor_input = MyTextInput(hint_text='Diretor do filme', font_size='20sp', size_hint=(0.15, 1))
        self.genero_input = MyTextInput(hint_text='Gênero do filme', font_size='20sp', size_hint=(0.15, 1))
        self.ano_input = MyTextInput(hint_text='Ano de lançamento do filme', font_size='20sp', size_hint=(0.15, 1))
        input_layout.add_widget(self.titulo_input)
        input_layout.add_widget(self.diretor_input)
        input_layout.add_widget(self.genero_input)
        input_layout.add_widget(self.ano_input)
        layout.add_widget(input_layout)

        # Botões
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
       # button_layout.add_widget(Button(text='Inserir na frente', font_size='21sp',on_press=self.inserir_na_frente, size_hint=(0.15, 1)))
        #button_layout.add_widget(Button(text='Inserir na fim', font_size='21sp' , on_press=self.insere_no_fim, size_hint=(0.15, 1)))
       # button_layout.add_widget(Button(text='Remove filme', font_size='21sp', on_press=self.remove_filme, size_hint=(0.15, 1)))
        for i in range(3):
            button_layout.add_widget(Button(text=f'Insere lista {i}', font_size='21sp', on_press=lambda instance, index=i: self.inserir_na_lista(index), size_hint=(0.15, 1)))
            button_layout.add_widget(Button(text=f'Remove lista {i}', font_size='21sp', on_press=lambda instance, index=i: self.remove_da_lista(index), size_hint=(0.15, 1)))
            button_layout.add_widget(Button(text=f'Exibe lista {i}', font_size='21sp', on_press=lambda instance, index=i: self.exibir_lista(index), size_hint=(0.15, 1)))
        layout.add_widget(button_layout)

        # Rótulo para exibir mensagem
        self.message_label = Label(text='', size_hint=(1, None), height=30)
        layout.add_widget(self.message_label)

        return layout

    def adicionar_filme(self, instance):
        titulo = self.titulo_input.text
        diretor = self.diretor_input.text
        genero = self.genero_input.text
        ano_lancamento = int(self.ano_input.text)

        novo_filme = Filme(titulo, diretor, genero, ano_lancamento)
        self.lista_filmes.insere_no_frente(novo_filme)

        # Atualiza o rótulo com a mensagem
        self.message_label.text = 'Filme adicionado: {} ({})'.format(titulo, ano_lancamento)

        self.titulo_input.text = ''
        self.diretor_input.text = ''
        self.genero_input.text = ''
        self.ano_input.text = ''
    
        
    def inserir_na_frente(self, instance):
        titulo = self.titulo_input.text
        diretor = self.diretor_input.text
        genero = self.genero_input.text
        ano_lancamento = int(self.ano_input.text)

        novo_filme = Filme(titulo, diretor, genero, ano_lancamento)
        self.lista_filmes.insere_no_frente(novo_filme)

        # Atualiza o rótulo com a mensagem
        self.message_label.text = 'Filme inserido na frente: {} ({})'.format(titulo, ano_lancamento)

        self.titulo_input.text = ''
        self.diretor_input.text = ''
        self.genero_input.text = ''
        self.ano_input.text = ''
        
    def insere_no_fim(self, instance):
        titulo = self.titulo_input.text
        diretor = self.diretor_input.text
        genero = self.genero_input.text
        ano_lancamento = int(self.ano_input.text)

        novo_filme = Filme(titulo, diretor, genero, ano_lancamento)
        self.lista_filmes.insere_no_fim(novo_filme)

        # Atualiza o rótulo com a mensagem
        self.message_label.text = 'Filme inserido na fim: {} ({})'.format(titulo, ano_lancamento)

        self.titulo_input.text = ''
        self.diretor_input.text = ''
        self.genero_input.text = ''
        self.ano_input.text = ''
    def remove_filme(self, instance):
        if self.lista_filmes.remove_do_inicio():
            self.message_label.text = 'Não há filmes para remover'
        else:
            self.message_label.text = 'Filme removido com sucesso. .'
    def exibir_lista_popup(self, instance):
        filmes = self.lista_filmes.exibe_lista()
        if isinstance(filmes, str):  # Verifica se a lista está vazia
            self.message_label.text = filmes
        else:
            content = BoxLayout(orientation='vertical')
            scrollview = ScrollView()
            list_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=5, padding=10)
            for i, filme in enumerate(filmes, start=1):
                label = Label(text='{} – {} ({}) - {}'.format(i, filme.titulo, filme.ano_lancamento, filme.diretor))
                list_layout.add_widget(label)
            scrollview.add_widget(list_layout)
            content.add_widget(scrollview)
            popup = Popup(title='Lista de Filmes', content=content, size_hint=(None, None), size=(400, 400))
            popup.open()

    def create_carousel(self):
            carousel_layout = BoxLayout(orientation='vertical')
            carousel = Carousel(direction='right', loop=True)  # Habilita o loop infinito
                
            src = [
                "src/imagem1.png", "src/imagem2.png", "src/imagem3.png",
                "src/imagem4.png", "src/imagem5.png", "src/imagem6.png",
                "src/imagem7.png", "src/imagem8.png", "src/imagem9.png",
                "src/imagem10.png", "src/imagem11.png","src/imagem12.png",
                "src/imagem13.png", "src/imagem14.png", "src/imagem15.png"
                
            ]
            for img_source in src:
                image = AsyncImage(source=img_source, allow_stretch=True, size_hint=(1, 1))
                carousel.add_widget(image)

            carousel_layout.add_widget(carousel)
            
            # Adiciona um título
            title_label = Label(text="Estrutura de Dados - Lista Circular\n", size_hint=(1, 0.067), height=10)
            title_label2 = Label(text="Profa. Dra.Mai-Ly Vanessa Almeida Saucedo Faro", size_hint=(1, None), height=0.75)
            carousel_layout.add_widget(title_label)
            carousel_layout.add_widget(title_label2)

            return carousel_layout

    def inserir_na_lista(self, indice_lista):
        titulo = self.titulo_input.text
        diretor = self.diretor_input.text
        genero = self.genero_input.text
        ano_lancamento = int(self.ano_input.text)

        novo_filme = Filme(titulo, diretor, genero, ano_lancamento)
        if self.multilista_filmes.insere_na_lista(indice_lista, novo_filme):
            self.message_label.text = f'Filme inserido na lista {indice_lista}'

        self.titulo_input.text = ''
        self.diretor_input.text = ''
        self.genero_input.text = ''
        self.ano_input.text = ''

    def remove_da_lista(self, indice_lista):
        if self.multilista_filmes.remove_da_lista(indice_lista):
            self.message_label.text = f'Filme removido da lista {indice_lista}'
        else:
            self.message_label.text = f'Lista {indice_lista} não existe'

    def exibir_lista(self, indice_lista):
        filmes = self.multilista_filmes.exibe_lista(indice_lista)
        if isinstance(filmes, str):  # Verifica se a lista está vazia
            self.message_label.text = filmes
        else:
            content = BoxLayout(orientation='vertical')
            scrollview = ScrollView()
            list_layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=5, padding=10)
            for i, filme in enumerate(filmes, start=1):
                label = Label(text=f'{i} – {filme.titulo} ({filme.ano_lancamento}) - {filme.diretor}')
                list_layout.add_widget(label)
            scrollview.add_widget(list_layout)
            content.add_widget(scrollview)
            popup = Popup(title=f'Lista de Filmes {indice_lista}', content=content, size_hint=(None, None), size=(400, 400))
            popup.open()

if __name__ == '__main__':
    FilmeApp().run()
