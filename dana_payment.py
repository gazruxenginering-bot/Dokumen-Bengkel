"""
DANA Payment Gateway Integration for Dokumen-Bengkel
Sandbox Configuration & Payment Processing
"""

import os
import json
import requests
import hashlib
import hmac
import time
from datetime import datetime
from typing import Dict, Optional, Tuple

# DANA Sandbox Configuration
DANA_CONFIG = {
    "sandbox": {
        "base_url": "https://api.sandbox.dana.id",
        "merchant_id": os.environ.get("DANA_MERCHANT_ID", "216620010026043209503"),
        "client_id": os.environ.get("DANA_CLIENT_ID", "2025112621324475258385"),
        "client_secret": os.environ.get("DANA_CLIENT_SECRET", "0320254759fb001aa2f48b2f941949eb39a817758c949a391fbc6709ec738f3b"),
        "public_key": os.environ.get("DANA_PUBLIC_KEY", "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw1kGzQWEKz9n1fBSLB0JLyknOejQcT6xCgSK0+PpAL+F2VfAIwZatlD7oGVFTeAA/g0esuRf8SEJ6mVCDdXQuauHeIKJYMYqrzoWr0B6j1GSjz0GgJ0ontPtLvfPgxI9qp5mafUzVq7iU9d6VGmk+hjCUbl2jHVgHmypwIbPwZ8tZ9uQi+Vq2gQXTMgCEljaX4GoBKkVgk5Iqv2csOz85QFFb5BHs/RE/anZLyVOwCaX2sI9GPIMMuvuAuHmI1ak2VaZ6YaAALUWGMVktZCRm10WcPlxe/j8mj/6IqmSU158tU6o4QuibWV7GkTMS3tI0o3HHgM2ixhmjX+ixQ/WfQIDAQAB"),
        "private_key": os.environ.get("DANA_PRIVATE_KEY", "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDDWQbNBYQrP2fV8FIsHQkvKSc56NBxPrEKBIrT4+kAv4XZV8AjBlq2UPugZUVN4AD+DR6y5F/xIQnqZUIN1dC5q4d4golgxiqvOhavQHqPUZKPPQaAnSie0+0u98+DEj2qnmZp9TNWruJT13pUaaT6GMJRuXaMdWAebKnAhs/Bny1n25CL5WraBBdMyAISWNpfgagEqRWCTkiq/Zyw7PzlAUVvkEez9ET9qdkvJU7AJpfawj0Y8gwy6+4C4eYjVqTZVpnphoAAtRYYxWS1kJGbXRZw+XF7+PyaP/oiqZJTXny1TqjhC6JtZXsaRMxLe0jSjcceAzaLGGaNf6LFD9Z9AgMBAAECggEAVxElANhGkmgORcJ5PYQrhcOX4i2sSe0hR0/C+LIKNfUnGToNPw8j+0KZBGJew1jl2FXMqvsy7+xD2R8Mk9IK19Zl6QZ1aJaqi7MeTTo15g77fbA7Z7OkWTYn7tkwukC1D4jOKMfK/AWyhp/xvBHiID5MzdQVzIC8OJNCDbeIfclFyNTQxNwW835+Tv2D4rKJXUzz0wntkyWiF3dIwaJ4mQEPrLkObIcltwRxQE5fH643ZZ6rIZfONGObnc4GSxD0PM/F1eVXQxIn2U9N9KhsKtQuMlFkEacqJ8CWa7W5ZdMcvikSk7Xju/kT/urBZLaal0aMJcw9HmnSfmBTgZ9TGQKBgQDGEPX2L8YHodAb1mM2WdODvwufVlOU7ca1fPi0/QTMCG5aB6Fj+TEoM5z8/Wu1l3/WxjehcVpA5zbHCek4Nz0RyeuH5zGSbL/g49zSn/jSVlLcrWHALX8GgpQGdgeQyKyxx/u9d4aWAV+Z14RKfzrGf5SrhQV6w+FhsbAZS53QcwKBgQD8fIHaba2qfjc6Cvb0xSMyfChEzY3QrMK0UOfk1m1H4Xwb/wUs6eG/7FWHpiIkR66h6p0Bj8OL4HiygKSl63m5FL8qSeOmf1COln7hu6brXBqj/5PrrxlLcm0qBt3xYnrxHCS559L75N+CyJdQHCVPtB9Fl57c1KsZwCTZFo+xTwKBgFE4xVRmdOPOVGQF/3tbTKSbJG373ZyWAUWNcQPvOhddYbtjo6g2mRTuTXNljNTTwqXVdRysOiGhb1Ih21SlOlLgJcj+YtKz69+SMYzh8wx2P9ak9w/y2ENYKtGXdzTFRiRFaRNiP3umJokU2vgdwoGB8fqAOyYDy5nfXuKQoq/HAoGAAL9VmxHsC68n9rIFnR/gRMv9SobZPp7kTKhYp2LDHA1c0rBkkYd3tZu7fRVO0JCtwajyIgkM6SMW+GBNHHif+Z5IGpXxaJLD6EglxAFMMzIomgetpmr0Rjbmf9NZYNeLyZ7ttOcsxrYcu0Rgvkn3Ck9cMFaMj9bJUuAwu7vHXR0CgYBeERamMyDBiyJzFraopcxYod+4pOc838evJ5u8po0S9XZdNOAlcBotPoMZJJJOSmWY5EDSJWllSE6GAOY6TCAOPLMO7qkzwlA1xV7QP/kuN5FfLNggYjxFmcNFwKaXCxlOW0uaDDJY37yWWoQrWYdqGDgazSB0QovnfFw6CFKA5A==")
    }
}


class DANAPaymentGateway:
    """DANA Payment Gateway Integration for Dokumen-Bengkel"""
    
    def __init__(self, environment: str = "sandbox"):
        self.env = environment
        self.config = DANA_CONFIG[environment]
        self.base_url = self.config["base_url"]
        self.merchant_id = self.config["merchant_id"]
        self.client_id = self.config["client_id"]
        self.client_secret = self.config["client_secret"]
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self) -> Optional[str]:
        """
        Get OAuth2 Access Token from DANA
        """
        if self.access_token and self.token_expiry and time.time() < self.token_expiry:
            return self.access_token
        
        token_url = f"{self.base_url}/oauth2/token"
        
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "payment.write"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            response = requests.post(token_url, data=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get("access_token")
            self.token_expiry = time.time() + data.get("expires_in", 3600) - 60  # Refresh 60s before expiry
            
            return self.access_token
        except Exception as e:
            print(f"Error getting DANA access token: {e}")
            return None
    
    def generate_signature(self, data: str, method: str = "SHA256") -> str:
        """
        Generate HMAC signature for request
        """
        if method == "SHA256":
            return hashlib.sha256(
                (data + self.client_secret).encode()
            ).hexdigest()
        return None
    
    def create_payment_order(self, 
                            order_id: str,
                            amount: float,
                            title: str,
                            description: str,
                            notify_url: str,
                            return_url: str) -> Dict:
        """
        Create payment order/invoice with DANA
        
        Args:
            order_id: Unique order identifier
            amount: Amount in IDR
            title: Payment title
            description: Payment description
            notify_url: Webhook URL for notifications
            return_url: Return URL after payment
        
        Returns:
            Dict with payment URL and order details
        """
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "Failed to get access token"}
        
        url = f"{self.base_url}/payment/orders/v1/create"
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        payload = {
            "merchantId": self.merchant_id,
            "orderId": order_id,
            "orderTitle": title,
            "orderDescription": description,
            "orderAmount": {
                "value": str(int(amount * 100)),  # Convert to cents
                "currency": "IDR"
            },
            "merchantUserId": "user_123",  # Can be customized
            "redirectUrl": return_url,
            "notifyUrl": notify_url,
            "timestamp": timestamp
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Merchant-Id": self.merchant_id,
            "X-Client-Id": self.client_id,
            "X-Timestamp": timestamp
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                "success": True,
                "order_id": order_id,
                "payment_url": data.get("paymentUrl"),
                "dana_order_id": data.get("orderId"),
                "created_at": timestamp
            }
        except Exception as e:
            print(f"Error creating payment order: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def verify_payment(self, order_id: str, dana_transaction_id: str) -> Dict:
        """
        Verify payment status with DANA
        """
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "Failed to get access token"}
        
        url = f"{self.base_url}/payment/orders/v1/{order_id}/status"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Merchant-Id": self.merchant_id,
            "X-Client-Id": self.client_id
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return {
                "success": True,
                "status": data.get("status"),
                "amount": data.get("orderAmount"),
                "verified": data.get("status") == "COMPLETED"
            }
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
dana_gateway = DANAPaymentGateway(environment="sandbox")
