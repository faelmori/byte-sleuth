![ByteSleuth_Banner](/docs/assets/top_banner_a.png)

# 🕵️‍♂️ **ByteSleuth** — Caçador de Caracteres Ocultos

> "Elementar, meu caro dev. Os fantasmas dos caracteres ocultos não escaparão desta auditoria!"
> — **CharlockHolmes**, o detetive dentro do ByteSleuth

ByteSleuth é um **scanner poderoso de caracteres Unicode & ASCII** projetado para detectar ofuscação, ameaças invisíveis e bytes suspeitos em textos ou códigos. Seja caçando **caracteres fantasmas** ou analisando **problemas de codificação**, o ByteSleuth garante um resultado **limpo e transparente**.

---

## 🚀 **Principais Funcionalidades**
- ✅ Detecta **caracteres de controle ASCII** (ex: `NUL`, `BEL`, `ESC`)
- ✅ Aponta **Unicode invisíveis** e **controles de direção** (ex: `U+200B`, `U+202E`)
- ✅ **Sanitiza** opcionalmente removendo caracteres ocultos/maliciosos
- ✅ Funciona com **arquivos**, **diretórios** e **stdin/PIPE**
- ✅ Suporte a **logs** para auditoria
- ✅ Gera **hash SHA256** antes/depois da sanitização
- ✅ Gera **relatórios JSON** (stdout ou arquivo)
- ✅ **Varredura concorrente** de diretórios
- ✅ Modo **fail-on-detect** para CI/CD/pre-commit
- ✅ **Backup/restauração** antes da sanitização
- ✅ **Extensão VSCode** para integração fácil
- ✅ Exemplos de integração com **pre-commit** e **CI/CD**
- ✅ **Exemplos reais** inclusos

---

## 🔧 **Uso via CLI**

```bash
python src/byte_sleuth.py <alvo> [opções]
```

### **Opções da CLI**
| Opção | Descrição |
|-------|-----------|
| `alvo` | Arquivo ou diretório a ser escaneado (ou use PIPE) |
| `-s`, `--sanitize` | Remove automaticamente caracteres suspeitos |
| `-l`, `--log` | Arquivo de log (padrão: `scanner.log`) |
| `-r`, `--report [arquivo]` | Imprime relatório JSON no stdout ou salva em arquivo |
| `-f`, `--no-backup` | Desativa criação de backup |
| `-v`, `--verbose` | Saída detalhada (hashes, achados) |
| `-d`, `--debug` | Saída de debug |
| `-q`, `--quiet` | Suprime toda saída exceto erros |
| `-S`, `--sanitize-only` | Apenas sanitiza, não escaneia/relata |
| `-F`, `--fail-on-detect` | Sai com código 1 se encontrar caracteres suspeitos |
| `-V`, `--version` | Mostra a versão e sai |

### **Exemplos de uso**
```bash
# Escaneia e sanitiza um arquivo, mostrando hashes e achados
python byte_sleuth/byte_sleuth.py arquivo.txt -s -v

# Escaneia um diretório, gera relatório JSON em arquivo
python byte_sleuth/byte_sleuth.py ./dados/ -r relatorio.json

# Sanitiza stdin (PIPE), saída para limpo.txt
cat arquivo.txt | python byte_sleuth/byte_sleuth.py -s > limpo.txt

# Escaneia via PIPE e falha (exit 1) se encontrar caractere suspeito (para CI/pre-commit)
cat arquivo.txt | python byte_sleuth/byte_sleuth.py -F

# Loga todos os caracteres removidos do PIPE em um log customizado
cat arquivo.txt | python byte_sleuth/byte_sleuth.py -s -l removidos.log > limpo.txt

# Escaneia diretório e falha se algum arquivo tiver caracteres suspeitos (CI/pre-commit)
python byte_sleuth/byte_sleuth.py src/ -F
```

---

## 📦 **Usando ByteSleuth em Projetos Python**

### **Instalação**
Assim que publicado no PyPI:
```bash
pip install byte-sleuth
```

### **Uso básico em Python**
```python
from byte_sleuth import ByteSleuth
scanner = ByteSleuth(sanitize=True)
achados = scanner.scan_file("exemplo.txt")
for cp, nome, char, idx in achados:
    print(f"⚠️ Caractere suspeito: {nome} (U+{cp:04X}) na posição {idx} → {repr(char)}")
```

---

## 🔁 **Automação & Integração**
- **Pre-commit hook**: Bloqueia commits com caracteres ocultos
- **CI/CD**: Falha builds se houver problemas
- **Extensão VSCode**: Escaneia arquivos abertos com um clique
- **Relatórios JSON**: Para auditoria ou automação

### **Exemplo de pre-commit**
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: byte-sleuth-scan
      name: ByteSleuth Unicode & ASCII Scanner
      entry: python src/byte_sleuth.py src/ -F
      language: system
      pass_filenames: false
```

### **Exemplo GitHub Actions**
```yaml
- name: Escanear caracteres ocultos
  run: cat arquivo.txt | python byte_sleuth/byte_sleuth.py -F
```

---

## 🧑‍💻 **Extensão VSCode**
- Escaneia o arquivo aberto para caracteres ocultos/suspeitos
- Resultados direto no VSCode
- Fácil de instalar e usar (veja `vscode-extension/README.md`)

---

## 🧠 **Por que usar ByteSleuth?**
Alguns caracteres são **invisíveis mas perigosos**—causam confusão em **código, configs ou documentos**. Vetores comuns:
- Espaços de largura zero para ofuscação
- Caracteres de direção bidirecional
- Códigos de controle ASCII ocultos
- Truques de formatação que atrapalham debugging e diffs

ByteSleuth te dá uma **lupa de detetive** para expor todos eles. 🔍

---

## 🚀 **Roadmap**
- [x] Métodos de sanitização expandidos
- [x] CLI interativa aprimorada
- [x] Relatórios JSON
- [x] Extensão VSCode
- [x] Changelog publicado
- [ ] Relatórios HTML
- [ ] Suporte a mais formatos (zip, PDF, etc.)
- [ ] Roadmap público

---

## 📄 **Licença**
MIT — *Use e compartilhe à vontade!*
