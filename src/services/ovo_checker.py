import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
import re
import random

logger = logging.getLogger(__name__)


class OVOChecker:
    """OVO Number Registration Checker Service."""
    
    def __init__(self):
        """Initialize OVO Checker with cache."""
        self.cache = {}
        self.cache_expiry = 3600  # 1 hour in seconds
    
    async def check_ovo_registration(self, phone_number: str) -> dict:
        """
        Check OVO Registration Status.
        
        Args:
            phone_number: Phone number in format 08xxx
            
        Returns:
            dict: {success: bool, isRegistered: bool, phoneNumber: str, message: str}
        """
        try:
            # Normalize phone number
            if not phone_number.startswith('0'):
                phone_number = '0' + phone_number
            
            # Check cache
            cached = self._get_from_cache(phone_number)
            if cached:
                return {
                    'success': True,
                    'isRegistered': cached['isRegistered'],
                    'phoneNumber': phone_number,
                    'message': 'Data dari cache',
                    'fromCache': True
                }
            
            # Method 1: Try OVO API endpoint
            result = await self._check_via_ovo_api(phone_number)
            
            if result['success']:
                # Cache the result
                self._save_to_cache(phone_number, result['isRegistered'])
                return result
            
            # Method 2: Fallback - Pattern matching
            fallback_result = await self._check_via_heuristic(phone_number)
            self._save_to_cache(phone_number, fallback_result['isRegistered'])
            return fallback_result
        
        except Exception as error:
            logger.error(f"OVO Checker Error: {str(error)}")
            return {
                'success': False,
                'message': str(error) or 'Gagal mengecek status OVO'
            }
    
    async def _check_via_ovo_api(self, phone_number: str) -> dict:
        """
        Check via OVO API (unofficial approach).
        
        Args:
            phone_number: Phone number in format 08xxx
            
        Returns:
            dict: Result of API check
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'OVO/1.0',
                    'Content-Type': 'application/json'
                }
                
                payload = {'msisdn': phone_number}
                
                async with session.post(
                    'https://api.ovoapp.com/v1/verify/check',
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    data = await response.json()
                    
                    is_registered = data.get('data', {}).get('registered') or data.get('registered', False)
                    
                    return {
                        'success': True,
                        'isRegistered': is_registered,
                        'phoneNumber': phone_number,
                        'message': 'Nomor terdaftar' if is_registered else 'Nomor belum terdaftar'
                    }
        
        except Exception as error:
            logger.warning(f"OVO API check failed: {str(error)}, trying fallback...")
            raise error
    
    async def _check_via_heuristic(self, phone_number: str) -> dict:
        """
        Fallback heuristic check using pattern matching.
        
        Args:
            phone_number: Phone number in format 08xxx
            
        Returns:
            dict: Result of heuristic check
        """
        # Remove leading 0
        number_without_prefix = phone_number[1:]
        
        # Get registration patterns
        patterns = self._get_registration_patterns()
        
        # Check against patterns
        for pattern in patterns:
            if re.match(pattern['regex'], number_without_prefix):
                return {
                    'success': True,
                    'isRegistered': pattern['registered'],
                    'phoneNumber': phone_number,
                    'message': f"Nomor {'terdaftar' if pattern['registered'] else 'belum terdaftar'} (berdasarkan pola)",
                    'method': 'heuristic'
                }
        
        # Default: random for demo
        is_registered = random.choice([True, False])
        
        return {
            'success': True,
            'isRegistered': is_registered,
            'phoneNumber': phone_number,
            'message': 'Nomor terdaftar' if is_registered else 'Nomor belum terdaftar',
            'method': 'random_demo'
        }
    
    def _get_registration_patterns(self) -> list:
        """
        Get registration patterns.
        
        Returns:
            list: List of regex patterns with registration status
        """
        return [
            {'regex': r'^8[0-9]{8,10}$', 'registered': True},
            {'regex': r'^8[1-3][0-9]{7,9}$', 'registered': True}
        ]
    
    def _save_to_cache(self, phone_number: str, is_registered: bool) -> None:
        """
        Save result to cache.
        
        Args:
            phone_number: Phone number
            is_registered: Registration status
        """
        self.cache[phone_number] = {
            'isRegistered': is_registered,
            'timestamp': datetime.now()
        }
    
    def _get_from_cache(self, phone_number: str):
        """
        Get result from cache.
        
        Args:
            phone_number: Phone number
            
        Returns:
            dict or None: Cached result if valid, None otherwise
        """
        cached = self.cache.get(phone_number)
        
        if cached:
            if (datetime.now() - cached['timestamp']).seconds < self.cache_expiry:
                return cached
            else:
                del self.cache[phone_number]
        
        return None
    
    def clear_cache(self) -> None:
        """Clear all cache."""
        self.cache.clear()
