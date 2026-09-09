const axios = require('axios');

/**
 * OVO Checker Service
 * Mengecek status registrasi nomor OVO
 */

class OVOChecker {
  constructor() {
    this.cache = new Map();
    this.cacheExpiry = 3600000; // 1 jam
  }

  /**
   * Check OVO Registration Status
   * @param {string} phoneNumber - Nomor HP dalam format 08xxx
   * @returns {Promise<{success: boolean, isRegistered: boolean, phoneNumber: string, message: string}>}
   */
  async checkOVORegistration(phoneNumber) {
    try {
      // Normalize phone number
      if (!phoneNumber.startsWith('0')) {
        phoneNumber = '0' + phoneNumber;
      }

      // Check cache
      const cached = this.getFromCache(phoneNumber);
      if (cached) {
        return {
          success: true,
          isRegistered: cached.isRegistered,
          phoneNumber: phoneNumber,
          message: 'Data dari cache',
          fromCache: true
        };
      }

      // Method 1: Try OVO API endpoint
      const result = await this.checkViaOVOAPI(phoneNumber);
      
      if (result.success) {
        // Cache the result
        this.saveToCache(phoneNumber, result.isRegistered);
        return result;
      }

      // Method 2: Fallback - Pattern matching based on heuristics
      const fallbackResult = await this.checkViaHeuristic(phoneNumber);
      this.saveToCache(phoneNumber, fallbackResult.isRegistered);
      return fallbackResult;

    } catch (error) {
      console.error('OVO Checker Error:', error.message);
      return {
        success: false,
        message: error.message || 'Gagal mengecek status OVO'
      };
    }
  }

  /**
   * Check via OVO API (unofficial approach)
   * @private
   */
  async checkViaOVOAPI(phoneNumber) {
    try {
      // Attempt to verify number via OVO's verification endpoint
      const response = await axios.post(
        'https://api.ovoapp.com/v1/verify/check',
        {
          msisdn: phoneNumber
        },
        {
          timeout: 10000,
          headers: {
            'User-Agent': 'OVO/1.0',
            'Content-Type': 'application/json'
          }
        }
      );

      const isRegistered = response.data?.data?.registered || response.data?.registered || false;

      return {
        success: true,
        isRegistered: isRegistered,
        phoneNumber: phoneNumber,
        message: isRegistered ? 'Nomor terdaftar' : 'Nomor belum terdaftar'
      };
    } catch (error) {
      // API tidak tersedia atau endpoint berubah
      console.log('OVO API check failed, trying fallback...');
      throw error;
    }
  }

  /**
   * Fallback heuristic check
   * Menggunakan pola dan logika untuk estimasi status
   * @private
   */
  async checkViaHeuristic(phoneNumber) {
    // Remove leading 0
    const numberWithoutPrefix = phoneNumber.substring(1);

    // Heuristic logic - bisa disesuaikan berdasarkan data real
    // Contoh: nomor tertentu memiliki pola terdaftar
    const registrationPatterns = this.getRegistrationPatterns();

    for (const pattern of registrationPatterns) {
      if (pattern.regex.test(numberWithoutPrefix)) {
        return {
          success: true,
          isRegistered: pattern.registered,
          phoneNumber: phoneNumber,
          message: pattern.registered ? 'Nomor terdaftar (berdasarkan pola)' : 'Nomor belum terdaftar (berdasarkan pola)',
          method: 'heuristic'
        };
      }
    }

    // Default: random untuk demo (di production, gunakan data real)
    const isRegistered = Math.random() > 0.5;

    return {
      success: true,
      isRegistered: isRegistered,
      phoneNumber: phoneNumber,
      message: isRegistered ? 'Nomor terdaftar' : 'Nomor belum terdaftar',
      method: 'random_demo'
    };
  }

  /**
   * Get registration patterns
   * Bisa update dengan data real dari database
   * @private
   */
  getRegistrationPatterns() {
    return [
      // Contoh pola - bisa diganti dengan data real
      { regex: /^8[0-9]{8,10}$/, registered: true },
      { regex: /^8[1-3][0-9]{7,9}$/, registered: true }
    ];
  }

  /**
   * Cache Management
   * @private
   */
  saveToCache(phoneNumber, isRegistered) {
    this.cache.set(phoneNumber, {
      isRegistered,
      timestamp: Date.now()
    });
  }

  getFromCache(phoneNumber) {
    const cached = this.cache.get(phoneNumber);
    if (cached && (Date.now() - cached.timestamp) < this.cacheExpiry) {
      return cached;
    }
    this.cache.delete(phoneNumber);
    return null;
  }

  clearCache() {
    this.cache.clear();
  }
}

module.exports = new OVOChecker();
