# .projeto_impressao_cupom


echo "# .projeto_impressao_cupom" >> README.md 

git init
git add README.md
git add .
git add --all 
git commit -m "Init: Inicio do Projeto"
git branch -M main 
git remote add origin https://github.com/eduardoangelis/.projeto_impressao_cupom.git
git push -u origin main
git status
git branch


# branch
main      produção
dev         recursos
stage       pre-produçao
feature

git init
git remote add origin https://github.com/eduardoangelis/projeto_ped_gestores.git
git add .
git add --all
git commit -m "Init: Inicio do Projeto"
git branch -M main
git push -u origin main
git status
git branch




# GIT

Config: a mudanças nas configurações do sistema, como ajustes em variáveis de ambiente, parâmetros de inicialização, configurações de banco de dados, entre outros.
Features: Usado para adição de uma nova funcionalidade ao sistema
Fix: Usado para commits que corrigem bugs ou problemas.
Docs: Para commits relacionados à documentação.
Style: Relacionado a mudanças de estilo de código, como formatação, espaçamento, etc.
Test: Para adição ou modificação de testes.
Chore: Usado para commits relacionados a tarefas de manutenção, como ajustes no sistema de build, atualizações de dependências, etc.
Performance: Para commits que melhoram o desempenho do código.
Security: Para commits que abordam questões de segurança.
Release: Para commits relacionados a lançamentos de versões.
Deprecation: Indica a depreciação de um recurso ou funcionalidade.
Refactor: Similar a "refacture", usado para commits que envolvem refatoração de código sem alterar seu comportamento externo.