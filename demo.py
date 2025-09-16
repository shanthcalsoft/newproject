#!/usr/bin/env python3
"""
Demo script to showcase cryptocurrency comparison features
"""

from crypto_analyzer import CryptoAnalyzer

def main():
    print("🚀 Cryptocurrency Comparison Demo 🚀")
    print("=" * 50)
    
    analyzer = CryptoAnalyzer(use_mock_data=True)
    
    # Demo 1: Get top cryptocurrencies
    print("\n1️⃣ Fetching top 20 cryptocurrencies...")
    cryptos = analyzer.fetch_top_cryptocurrencies(20)
    analyzer.display_crypto_table(cryptos, 10)
    
    # Demo 2: Show recommendations
    print("\n2️⃣ Analyzing best investment opportunities...")
    recommendations = analyzer.analyze_best_opportunities(cryptos)
    analyzer.display_recommendations(recommendations)
    
    # Demo 3: Compare specific cryptocurrencies
    print("\n3️⃣ Comparing BTC, ETH, and SOL...")
    comparison = analyzer.get_specific_crypto_analysis(['BTC', 'ETH', 'SOL'])
    
    if 'error' not in comparison:
        for symbol, data in comparison.items():
            print(f"\n{symbol} ({data['name']}):")
            print(f"  💰 Price: ${data['price']:,.4f}")
            print(f"  🏆 Rank: #{data['rank']}")
            print(f"  📈 24h Change: {data['change_24h']:.2f}%")
            print(f"  💎 Market Cap: ${data['market_cap']:,}")
            print(f"  💡 {data['recommendation']}")
    
    # Demo 4: Save analysis report
    print("\n4️⃣ Saving analysis report...")
    analyzer.save_analysis_report(cryptos, recommendations)
    
    print(f"\n✅ Demo completed successfully!")

if __name__ == "__main__":
    main()