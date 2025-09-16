#!/usr/bin/env python3
"""
Cryptocurrency Price Comparison and Selection Tool with Mock Data

This tool helps users compare cryptocurrency prices and make informed decisions
about which cryptocurrencies to potentially purchase based on various metrics.
"""

import json
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from tabulate import tabulate
import pandas as pd
from colorama import Fore, Style, init
from datetime import datetime
import random

# Initialize colorama for cross-platform colored output
init()


@dataclass
class CryptoData:
    """Data class to hold cryptocurrency information"""
    id: str
    symbol: str
    name: str
    current_price: float
    market_cap: int
    market_cap_rank: int
    total_volume: int
    price_change_24h: float
    price_change_percentage_24h: float
    circulating_supply: float
    total_supply: Optional[float]
    max_supply: Optional[float]


class MockDataProvider:
    """Provides mock cryptocurrency data when live API is not available"""
    
    @staticmethod
    def get_mock_crypto_data() -> List[Dict]:
        """Generate realistic mock cryptocurrency data"""
        cryptos = [
            {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "rank": 1, "base_price": 43500},
            {"id": "ethereum", "symbol": "eth", "name": "Ethereum", "rank": 2, "base_price": 2650},
            {"id": "tether", "symbol": "usdt", "name": "Tether", "rank": 3, "base_price": 1.00},
            {"id": "binancecoin", "symbol": "bnb", "name": "BNB", "rank": 4, "base_price": 315},
            {"id": "solana", "symbol": "sol", "name": "Solana", "rank": 5, "base_price": 98},
            {"id": "ripple", "symbol": "xrp", "name": "XRP", "rank": 6, "base_price": 0.52},
            {"id": "usd-coin", "symbol": "usdc", "name": "USDC", "rank": 7, "base_price": 1.00},
            {"id": "staked-ether", "symbol": "steth", "name": "Lido Staked Ether", "rank": 8, "base_price": 2645},
            {"id": "cardano", "symbol": "ada", "name": "Cardano", "rank": 9, "base_price": 0.45},
            {"id": "avalanche-2", "symbol": "avax", "name": "Avalanche", "rank": 10, "base_price": 36},
            {"id": "dogecoin", "symbol": "doge", "name": "Dogecoin", "rank": 11, "base_price": 0.082},
            {"id": "chainlink", "symbol": "link", "name": "Chainlink", "rank": 12, "base_price": 14.5},
            {"id": "polkadot", "symbol": "dot", "name": "Polkadot", "rank": 13, "base_price": 6.8},
            {"id": "polygon", "symbol": "matic", "name": "Polygon", "rank": 14, "base_price": 0.87},
            {"id": "uniswap", "symbol": "uni", "name": "Uniswap", "rank": 15, "base_price": 8.2},
            {"id": "litecoin", "symbol": "ltc", "name": "Litecoin", "rank": 16, "base_price": 74},
            {"id": "internet-computer", "symbol": "icp", "name": "Internet Computer", "rank": 17, "base_price": 12.5},
            {"id": "near", "symbol": "near", "name": "NEAR Protocol", "rank": 18, "base_price": 2.1},
            {"id": "aptos", "symbol": "apt", "name": "Aptos", "rank": 19, "base_price": 8.9},
            {"id": "stellar", "symbol": "xlm", "name": "Stellar", "rank": 20, "base_price": 0.105}
        ]
        
        mock_data = []
        for crypto in cryptos:
            # Add some realistic variation to prices
            price_variation = random.uniform(-0.15, 0.15)  # ±15% variation
            current_price = crypto["base_price"] * (1 + price_variation)
            
            # Calculate realistic market cap based on price and typical supply
            if crypto["symbol"] == "btc":
                circulating_supply = 19_500_000
            elif crypto["symbol"] == "eth":
                circulating_supply = 120_000_000
            elif crypto["symbol"] in ["usdt", "usdc"]:
                circulating_supply = random.randint(80_000_000_000, 120_000_000_000)
            elif crypto["symbol"] == "xrp":
                circulating_supply = 53_000_000_000
            elif crypto["symbol"] == "ada":
                circulating_supply = 35_000_000_000
            elif crypto["symbol"] == "doge":
                circulating_supply = 143_000_000_000
            else:
                circulating_supply = random.randint(100_000_000, 10_000_000_000)
            
            market_cap = int(current_price * circulating_supply)
            
            # Generate 24h price change
            price_change_24h_pct = random.uniform(-8, 12)  # -8% to +12%
            price_change_24h = current_price * (price_change_24h_pct / 100)
            
            # Generate volume (typically 1-20% of market cap for major coins)
            volume_ratio = random.uniform(0.01, 0.2)
            total_volume = int(market_cap * volume_ratio)
            
            mock_data.append({
                'id': crypto['id'],
                'symbol': crypto['symbol'],
                'name': crypto['name'],
                'current_price': current_price,
                'market_cap': market_cap,
                'market_cap_rank': crypto['rank'],
                'total_volume': total_volume,
                'price_change_24h': price_change_24h,
                'price_change_percentage_24h': price_change_24h_pct,
                'circulating_supply': circulating_supply,
                'total_supply': circulating_supply * random.uniform(1.0, 1.5) if crypto['symbol'] not in ['usdt', 'usdc'] else circulating_supply,
                'max_supply': None if crypto['symbol'] in ['eth', 'usdt', 'usdc'] else circulating_supply * random.uniform(1.1, 2.0)
            })
        
        return mock_data


class CryptoAnalyzer:
    """Main class for cryptocurrency analysis and comparison"""
    
    def __init__(self, use_mock_data: bool = False):
        self.use_mock_data = use_mock_data
        
    def fetch_top_cryptocurrencies(self, limit: int = 50) -> List[CryptoData]:
        """
        Fetch top cryptocurrencies by market cap
        
        Args:
            limit: Number of cryptocurrencies to fetch (default: 50)
            
        Returns:
            List of CryptoData objects
        """
        if self.use_mock_data:
            # Use mock data
            data = MockDataProvider.get_mock_crypto_data()[:limit]
        else:
            # In a real implementation, this would use the API
            # For now, fallback to mock data
            print(f"{Fore.YELLOW}Note: Using mock data for demonstration{Style.RESET_ALL}")
            data = MockDataProvider.get_mock_crypto_data()[:limit]
        
        crypto_list = []
        for item in data:
            crypto = CryptoData(
                id=item['id'],
                symbol=item['symbol'].upper(),
                name=item['name'],
                current_price=item['current_price'],
                market_cap=item['market_cap'],
                market_cap_rank=item['market_cap_rank'],
                total_volume=item['total_volume'],
                price_change_24h=item['price_change_24h'],
                price_change_percentage_24h=item['price_change_percentage_24h'],
                circulating_supply=item['circulating_supply'],
                total_supply=item['total_supply'],
                max_supply=item['max_supply']
            )
            crypto_list.append(crypto)
        
        return crypto_list
    
    def display_crypto_table(self, crypto_list: List[CryptoData], top_n: int = 20):
        """
        Display cryptocurrency data in a formatted table
        
        Args:
            crypto_list: List of CryptoData objects
            top_n: Number of top cryptocurrencies to display
        """
        if not crypto_list:
            print(f"{Fore.RED}No cryptocurrency data to display{Style.RESET_ALL}")
            return
        
        # Prepare data for table
        table_data = []
        for crypto in crypto_list[:top_n]:
            # Color code price changes
            change_color = Fore.GREEN if crypto.price_change_percentage_24h >= 0 else Fore.RED
            price_change = f"{change_color}{crypto.price_change_percentage_24h:.2f}%{Style.RESET_ALL}"
            
            table_data.append([
                crypto.market_cap_rank,
                crypto.symbol,
                crypto.name[:20],  # Truncate long names
                f"${crypto.current_price:,.4f}",
                f"${crypto.market_cap:,}",
                f"${crypto.total_volume:,}",
                price_change
            ])
        
        headers = [
            "Rank", "Symbol", "Name", "Price (USD)", 
            "Market Cap", "Volume (24h)", "Change (24h)"
        ]
        
        print(f"\n{Fore.CYAN}Top {top_n} Cryptocurrencies by Market Cap{Style.RESET_ALL}")
        print("=" * 90)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def analyze_best_opportunities(self, crypto_list: List[CryptoData]) -> List[CryptoData]:
        """
        Analyze and rank cryptocurrencies based on multiple criteria
        
        Args:
            crypto_list: List of CryptoData objects
            
        Returns:
            List of recommended cryptocurrencies
        """
        if not crypto_list:
            return []
        
        # Create DataFrame for easier analysis
        df_data = []
        for crypto in crypto_list:
            df_data.append({
                'symbol': crypto.symbol,
                'name': crypto.name,
                'price': crypto.current_price,
                'market_cap': crypto.market_cap,
                'volume': crypto.total_volume,
                'change_24h': crypto.price_change_percentage_24h,
                'rank': crypto.market_cap_rank,
                'crypto_obj': crypto
            })
        
        df = pd.DataFrame(df_data)
        
        # Scoring algorithm (you can customize these weights)
        df['stability_score'] = 100 - df['rank']  # Lower rank = higher stability
        df['volume_score'] = (df['volume'] / df['volume'].max()) * 100
        df['growth_potential'] = df['change_24h'].apply(
            lambda x: max(0, x * 2) if x > -5 else 0  # Positive but not overly volatile
        )
        
        # Combined score (customize weights as needed)
        df['total_score'] = (
            df['stability_score'] * 0.4 +
            df['volume_score'] * 0.3 +
            df['growth_potential'] * 0.3
        )
        
        # Sort by total score
        df_sorted = df.sort_values('total_score', ascending=False)
        
        # Return top recommendations
        recommended = []
        for _, row in df_sorted.head(10).iterrows():
            recommended.append(row['crypto_obj'])
        
        return recommended
    
    def display_recommendations(self, recommended: List[CryptoData]):
        """
        Display recommended cryptocurrencies with reasoning
        
        Args:
            recommended: List of recommended CryptoData objects
        """
        if not recommended:
            print(f"{Fore.RED}No recommendations available{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}🏆 TOP CRYPTOCURRENCY RECOMMENDATIONS 🏆{Style.RESET_ALL}")
        print("=" * 70)
        
        for i, crypto in enumerate(recommended[:5], 1):
            change_color = Fore.GREEN if crypto.price_change_percentage_24h >= 0 else Fore.RED
            
            print(f"\n{Fore.CYAN}#{i} {crypto.symbol} ({crypto.name}){Style.RESET_ALL}")
            print(f"   💰 Price: ${crypto.current_price:,.4f}")
            print(f"   📊 Market Cap Rank: #{crypto.market_cap_rank}")
            print(f"   📈 24h Change: {change_color}{crypto.price_change_percentage_24h:.2f}%{Style.RESET_ALL}")
            print(f"   💎 Market Cap: ${crypto.market_cap:,}")
            print(f"   🔄 Volume: ${crypto.total_volume:,}")
            
            # Simple recommendation reasoning
            reasons = []
            if crypto.market_cap_rank <= 10:
                reasons.append("Top 10 by market cap (high stability)")
            if crypto.price_change_percentage_24h > 0:
                reasons.append("Positive 24h performance")
            if crypto.total_volume > 1000000000:  # > 1B volume
                reasons.append("High trading volume (good liquidity)")
            if crypto.price_change_percentage_24h > 5:
                reasons.append("Strong upward momentum")
            
            if reasons:
                print(f"   ✅ Why recommended: {', '.join(reasons)}")
    
    def get_specific_crypto_analysis(self, symbols: List[str]) -> Dict:
        """
        Get detailed analysis for specific cryptocurrencies
        
        Args:
            symbols: List of cryptocurrency symbols (e.g., ['BTC', 'ETH'])
            
        Returns:
            Dictionary with analysis results
        """
        all_cryptos = self.fetch_top_cryptocurrencies(100)
        
        if not all_cryptos:
            return {}
        
        # Filter for requested symbols
        selected_cryptos = [
            crypto for crypto in all_cryptos 
            if crypto.symbol.upper() in [s.upper() for s in symbols]
        ]
        
        if not selected_cryptos:
            return {"error": "No matching cryptocurrencies found"}
        
        # Compare selected cryptocurrencies
        comparison = {}
        for crypto in selected_cryptos:
            comparison[crypto.symbol] = {
                "name": crypto.name,
                "price": crypto.current_price,
                "market_cap": crypto.market_cap,
                "rank": crypto.market_cap_rank,
                "change_24h": crypto.price_change_percentage_24h,
                "volume": crypto.total_volume,
                "recommendation": self._get_buy_recommendation(crypto)
            }
        
        return comparison
    
    def _get_buy_recommendation(self, crypto: CryptoData) -> str:
        """Generate a buy recommendation for a specific cryptocurrency"""
        score = 0
        reasons = []
        
        # Stability (market cap rank)
        if crypto.market_cap_rank <= 5:
            score += 30
            reasons.append("Top 5 market cap")
        elif crypto.market_cap_rank <= 10:
            score += 20
            reasons.append("Top 10 market cap")
        elif crypto.market_cap_rank <= 20:
            score += 10
            reasons.append("Top 20 market cap")
        
        # Recent performance
        if crypto.price_change_percentage_24h > 5:
            score += 25
            reasons.append("Strong recent gains")
        elif crypto.price_change_percentage_24h > 0:
            score += 15
            reasons.append("Positive momentum")
        elif crypto.price_change_percentage_24h > -5:
            score += 5
            reasons.append("Stable price")
        
        # Volume (liquidity)
        if crypto.total_volume > 5000000000:  # > 5B
            score += 20
            reasons.append("Very high liquidity")
        elif crypto.total_volume > 1000000000:  # > 1B
            score += 15
            reasons.append("High liquidity")
        elif crypto.total_volume > 100000000:  # > 100M
            score += 10
            reasons.append("Good liquidity")
        
        # Generate recommendation
        if score >= 60:
            recommendation = "🟢 STRONG BUY"
        elif score >= 40:
            recommendation = "🟡 BUY"
        elif score >= 20:
            recommendation = "🟠 HOLD/CONSIDER"
        else:
            recommendation = "🔴 CAUTION"
        
        return f"{recommendation} (Score: {score}/75) - {', '.join(reasons)}"
    
    def save_analysis_report(self, crypto_list: List[CryptoData], recommendations: List[CryptoData], filename: str = None):
        """Save analysis report to JSON file"""
        if filename is None:
            filename = f"crypto_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_cryptos_analyzed": len(crypto_list),
            "top_cryptos": [asdict(crypto) for crypto in crypto_list[:10]],
            "recommendations": [asdict(crypto) for crypto in recommendations[:5]]
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n{Fore.GREEN}📄 Analysis report saved to: {filename}{Style.RESET_ALL}")


def main():
    """Main function to run the cryptocurrency analyzer"""
    analyzer = CryptoAnalyzer(use_mock_data=True)
    
    print(f"{Fore.MAGENTA}🚀 Cryptocurrency Price Comparison & Selection Tool 🚀{Style.RESET_ALL}")
    print("=" * 70)
    
    # Fetch cryptocurrency data
    print(f"{Fore.YELLOW}Fetching cryptocurrency data...{Style.RESET_ALL}")
    crypto_list = analyzer.fetch_top_cryptocurrencies(20)
    
    if not crypto_list:
        print(f"{Fore.RED}Failed to fetch cryptocurrency data.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Display top cryptocurrencies
    analyzer.display_crypto_table(crypto_list, 20)
    
    # Analyze and display recommendations
    recommendations = analyzer.analyze_best_opportunities(crypto_list)
    analyzer.display_recommendations(recommendations)
    
    # Save analysis report
    analyzer.save_analysis_report(crypto_list, recommendations)
    
    # Interactive mode
    print(f"\n{Fore.CYAN}💡 Interactive Features:{Style.RESET_ALL}")
    print("1. Compare specific cryptocurrencies")
    print("2. Get detailed buy recommendations")
    print("3. Exit")
    
    while True:
        print(f"\n{Fore.GREEN}Choose an option (1-3) or enter symbols (e.g., BTC,ETH): {Style.RESET_ALL}", end="")
        user_input = input().strip()
        
        if user_input.lower() in ['3', 'quit', 'exit', 'q']:
            print(f"{Fore.YELLOW}Thank you for using the Crypto Analyzer! Happy trading! 📈{Style.RESET_ALL}")
            break
        elif user_input == '1':
            print("Enter cryptocurrency symbols separated by commas (e.g., BTC,ETH,ADA):")
            symbols_input = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
            if symbols_input:
                symbols = [s.strip() for s in symbols_input.split(',')]
                comparison = analyzer.get_specific_crypto_analysis(symbols)
                
                if 'error' in comparison:
                    print(f"{Fore.RED}{comparison['error']}{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.CYAN}📊 Detailed Comparison Results:{Style.RESET_ALL}")
                    for symbol, data in comparison.items():
                        change_color = Fore.GREEN if data['change_24h'] >= 0 else Fore.RED
                        print(f"\n{Fore.YELLOW}━━━ {symbol} ({data['name']}) ━━━{Style.RESET_ALL}")
                        print(f"💰 Price: ${data['price']:,.4f}")
                        print(f"🏆 Rank: #{data['rank']}")
                        print(f"📈 24h Change: {change_color}{data['change_24h']:.2f}%{Style.RESET_ALL}")
                        print(f"💎 Market Cap: ${data['market_cap']:,}")
                        print(f"🔄 Volume: ${data['volume']:,}")
                        print(f"💡 Recommendation: {data['recommendation']}")
        
        elif user_input == '2':
            print(f"\n{Fore.CYAN}🎯 Detailed Buy Recommendations for Top 5:{Style.RESET_ALL}")
            for i, crypto in enumerate(recommendations[:5], 1):
                recommendation = analyzer._get_buy_recommendation(crypto)
                change_color = Fore.GREEN if crypto.price_change_percentage_24h >= 0 else Fore.RED
                print(f"\n{i}. {crypto.symbol} ({crypto.name})")
                print(f"   💰 ${crypto.current_price:,.4f} | {change_color}{crypto.price_change_percentage_24h:.2f}%{Style.RESET_ALL}")
                print(f"   {recommendation}")
        
        elif ',' in user_input or user_input.upper() in ['BTC', 'ETH', 'ADA', 'SOL', 'XRP', 'DOGE', 'DOT', 'LINK', 'UNI', 'LTC']:
            # Direct symbol input
            symbols = [s.strip() for s in user_input.split(',')]
            if len(symbols) == 1 and ',' not in user_input:
                symbols = [user_input.strip()]
            
            comparison = analyzer.get_specific_crypto_analysis(symbols)
            
            if 'error' in comparison:
                print(f"{Fore.RED}{comparison['error']}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}📊 Quick Comparison:{Style.RESET_ALL}")
                for symbol, data in comparison.items():
                    change_color = Fore.GREEN if data['change_24h'] >= 0 else Fore.RED
                    print(f"\n{symbol}: ${data['price']:,.4f} | {change_color}{data['change_24h']:.2f}%{Style.RESET_ALL}")
                    print(f"   {data['recommendation']}")


if __name__ == "__main__":
    main()