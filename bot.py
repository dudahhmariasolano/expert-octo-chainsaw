mport logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

TOKEN = "8385589309:AAEFmuqO3I0I4ZeXm-XJrYWwkl7GSRxqBWY"
AFFILIATE_ID = "18318050413"

logging.basicConfig(level=logging.INFO)

AGUARDA_LINK, AGUARDA_NOME, AGUARDA_PRECO_DE, AGUARDA_PRECO_POR = range(4)

def converter_link(link):
    link = link.strip()
    if "?" in link:
        return f"{link}&affiliate_id={AFFILIATE_ID}"
    return f"{link}?affiliate_id={AFFILIATE_ID}"

def gerar_template(nome, preco_de, preco_por, link):
    return (
        f"EU SEI QUE VOCÊ PRECISA.🔥\n\n"
        f"🛍️ {nome}\n"
        f"De R$ {preco_de}\n"
        f"💸 Por R$ {preco_por}\n"
        f"🔥Compre aqui: {link}\n"
        f"⚠ Promoção sujeita a alteração a qualquer momento."
    )

async def start(update, context):
    await update.message.reply_text("👋 Me manda o link do produto da Shopee!")
    return AGUARDA_LINK

async def receber_link(update, context):
    context.user_data["link"] = converter_link(update.message.text)
    await update.message.reply_text("✅ Link recebido!\n\n📝 Agora me manda o *nome do produto:*", parse_mode="Markdown")
    return AGUARDA_NOME

async def receber_nome(update, context):
    context.user_data["nome"] = update.message.text.strip()
    await update.message.reply_text("💰 Qual o preço *original* (De)? Ex: `18,92`", parse_mode="Markdown")
    return AGUARDA_PRECO_DE

async def receber_preco_de(update, context):
    context.user_data["preco_de"] = update.message.text.strip()
    await update.message.reply_text("🔥 Qual o preço *com desconto* (Por)? Ex: `11,73`", parse_mode="Markdown")
    return AGUARDA_PRECO_POR

async def receber_preco_por(update, context):
    context.user_data["preco_por"] = update.message.text.strip()
    template = gerar_template(
        context.user_data["nome"],
        context.user_data["preco_de"],
        context.user_data["preco_por"],
        context.user_data["link"]
    )
    await update.message.reply_text("✅ Template pronto:\n\n" + "─"*30)
    await update.message.reply_text(template)
    await update.message.reply_text("🚀 Me manda outro link quando quiser!")
    return AGUARDA_LINK

async def cancelar(update, context):
    await update.message.reply_text("❌ Cancelado! Me manda um link quando quiser.")
    return AGUARDA_LINK

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start), MessageHandler(filters.TEXT & ~filters.COMMAND, receber_link)],
        states={
            AGUARDA_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_link)],
            AGUARDA_NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)],
            AGUARDA_PRECO_DE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_preco_de)],
            AGUARDA_PRECO_POR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_preco_por)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )
    app.add_handler(conv)
    print("🤖 Bot rodando!")
    app.run_polling()

if __name__ == "__main__":
    main()
