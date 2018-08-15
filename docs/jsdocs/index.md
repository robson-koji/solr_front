#   __Documentação JavaScript do projeto Solr Front__





## Sobre
  Esta documentação é gerada com a utilização do pacote Jsdoc 3. Para sua instalação use o comando, como root do sistema, ```npm install -g jsdoc```

  ### Dependencias
   + Node 4.8 ou superior
   + Jsdoc 3
    - Template minami
    - Template tui-jsdoc-template

## Templates

  Para utilização dos templates presentes no arquivo de configuração ```conf.js``` instale os seguintes pacotes como root:

  - ```npm install -g minami```  

  [o projeto pode ser conferido aqui](https://github.com/nijikokun/minami)

  - ```npm install -D -g tui-jsdoc-template```

  [o projeto pode ser conferido aqui](https://github.com/nhnent/tui.jsdoc-template)

  Qualquer outro novo template instalado via npm, deve ser instalado globalmente ```-g``` como root do sistema e incluir no arquivo de configuração o path do node_modules, global que é ```/usr/lib/node_modules/{{nome do template}}/```

## Como gerar a documentação

  Para gerar a documentação use o comando ```jsdoc -c jsdocs/conf.js``` a partir do diretorio raiz do projeto. Os diretorios build e tutoriais devem ser ciados manualmente dentro da pasta docs/jsdocs/*


  *Dica:*
  *Para evitar erros na compilção no momento de geração da documentação, certifique-se que na configuração o ultimo item de uma lista nunca tenha virgula.*


## Como documentar

 É necessário incluir o app django que deseja documentar na configuração conf.js

 __Exemplo__



    "source": {

      "include": [ "solr_front", "outro app", ...],
    }

  E então deve-se incluir em cada arquivo js do app, a tag ```/*@module AppName::FileName*/```

  Por fim utilize o formato de documentação Jsdoc em cada classe ou função que deseje documentar, para
  maiores informações sobre o formato de documentação acesse, [ES 2015 class](http://usejsdoc.org/howto-es2015-classes.html), [ES 2015 Modules](http://usejsdoc.org/howto-es2015-modules.html), [CommonJS Modules](http://usejsdoc.org/howto-commonjs-modules.html) e [AMD Modules](http://usejsdoc.org/howto-amd-modules.html)


## Tutoriais

  Crie e edite arquivos .md no diretório ```jsdocs/tutoriais```, os arquivos seram automaticamente incluidos na geração de documentação.

  Para incluir link para tutorial diretamente em uma classe ou função, utilize a Tag ```/*@tutorial nomeArquivoSemExtensão */```  mais informações em [@useJSDoc](http://usejsdoc.org/tags-inline-tutorial.html)
