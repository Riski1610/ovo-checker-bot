require('dotenv').config();
const { Telegraf } = require('telegraf');
const ovoChecker = require('./services/ovoChecker');

const bot = new Telegraf(process.env.TELEGRAM_TOKEN);

// Start command
bot.start((ctx) => {
  ctx.reply(
    '👋 Selamat datang di OVO Checker Bot!\n\n' +
    'Bot ini membantu Anda mengecek apakah nomor HP terdaftar di OVO atau belum.\n\n' +
    'Cara penggunaan:\n' +
    '📱 Kirim nomor HP (contoh: 081234567890)\n\n' +
    'Perintah:\n' +
    '/start - Tampilkan menu ini\n' +
    '/help - Bantuan\n' +
    '/about - Tentang bot',
    {
      parse_mode: 'HTML'
    }
  );
});

// Help command
bot.command('help', (ctx) => {
  ctx.reply(
    '📖 <b>Bantuan</b>\n\n' +
    '1. Kirim nomor HP yang ingin dicek\n' +
    '2. Bot akan memproses dan memberikan hasil\n' +
    '3. Hasil: ✅ Terdaftar atau ❌ Belum Terdaftar\n\n' +
    '<b>Format nomor:</b>\n' +
    '- 08xxxxxxxxxx (format Indonesia)\n' +
    '- +628xxxxxxxxxx (dengan kode negara)',
    {
      parse_mode: 'HTML'
    }
  );
});

// About command
bot.command('about', (ctx) => {
  ctx.reply(
    'ℹ️ <b>Tentang Bot</b>\n\n' +
    'OVO Checker Bot v1.0\n' +
    'Dibuat untuk mengecek status registrasi nomor OVO\n\n' +
    '⚠️ Disclaimer:\n' +
    'Bot ini hanya untuk keperluan verifikasi nomor OVO secara umum.',
    {
      parse_mode: 'HTML'
    }
  );
});

// Handle text messages (phone numbers)
bot.on('text', async (ctx) => {
  const userInput = ctx.message.text.trim();
  
  // Validate if input looks like a phone number
  if (!isPhoneNumber(userInput)) {
    return ctx.reply('❌ Format nomor tidak valid. Silakan kirim nomor HP yang benar (contoh: 081234567890)');
  }

  try {
    // Show typing indicator
    await ctx.sendChatAction('typing');
    
    // Normalize phone number
    const phoneNumber = normalizePhoneNumber(userInput);
    
    // Check OVO registration status
    ctx.reply('⏳ Sedang mengecek...');
    const result = await ovoChecker.checkOVORegistration(phoneNumber);
    
    // Send result
    if (result.success) {
      const statusEmoji = result.isRegistered ? '✅' : '❌';
      const statusText = result.isRegistered ? 'TERDAFTAR' : 'BELUM TERDAFTAR';
      
      ctx.reply(
        `${statusEmoji} <b>Hasil Pengecekan</b>\n\n` +
        `📱 Nomor: ${result.phoneNumber}\n` +
        `📊 Status: ${statusText}\n` +
        `⏰ Waktu: ${new Date().toLocaleString('id-ID')}`,
        {
          parse_mode: 'HTML'
        }
      );
    } else {
      ctx.reply(`❌ Error: ${result.message}`);
    }
  } catch (error) {
    console.error('Error:', error);
    ctx.reply('❌ Terjadi kesalahan. Silakan coba lagi nanti.');
  }
});

// Error handler
bot.catch((err, ctx) => {
  console.error('Bot Error:', err);
  ctx.reply('❌ Terjadi kesalahan pada bot.');
});

// Helper functions
function isPhoneNumber(input) {
  // Check if input contains only numbers and optional + sign
  const phoneRegex = /^(\+62|62|0)[0-9]{9,12}$/;
  return phoneRegex.test(input.replace(/\s/g, ''));
}

function normalizePhoneNumber(phone) {
  // Remove spaces and convert to standard format
  phone = phone.replace(/\s/g, '');
  
  // Convert to 0 prefix format
  if (phone.startsWith('+62')) {
    return '0' + phone.slice(3);
  } else if (phone.startsWith('62')) {
    return '0' + phone.slice(2);
  }
  
  return phone;
}

// Start bot
bot.launch();

console.log('🤖 OVO Checker Bot is running...');

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
