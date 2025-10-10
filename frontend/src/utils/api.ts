// API configuration utility
import axios from 'axios'

export const getApiBaseUrl = (): string => {
  // In production (Render.com), use the backend service URL
  if (import.meta.env.PROD) {
    return 'https://tokyo-weekender-seo-dashboard-backend.onrender.com/api'
  }
  
  // In development, use localhost
  return 'http://localhost:8000/api'
}

// Mock data for when backend is not available
const getMockData = (endpoint: string): any => {
  // Remove query parameters for matching
  const cleanEndpoint = endpoint.split('?')[0]
  
  switch (cleanEndpoint) {
    case '/api/analysis/summary':
      return {
        total_keywords: 60872,
        total_volume: 2450000,
        total_traffic: 45000,
        avg_position: 28.5,
        top_performing_keywords: 1250
      }
    case '/api/analysis/performance':
      return {
        position_distribution: {
          top_3: { count: 850, total_traffic: 12000 },
          top_10: { count: 1250, total_traffic: 18000 },
          top_20: { count: 2100, total_traffic: 8000 },
          top_50: { count: 3500, total_traffic: 3000 },
          not_ranking: { count: 53172, total_traffic: 0 }
        }
      }
    case '/api/analysis/serp-features':
      return {
        'Featured Snippets': { count: 450 },
        'People Also Ask': { count: 320 },
        'Image Pack': { count: 280 },
        'Local Pack': { count: 150 },
        'Video': { count: 120 }
      }
    case '/api/competitors/summary':
      return {
        competitors: [
          {
            site_name: 'tokyocheapo.com',
            display_name: 'Tokyo Cheapo',
            total_keywords: 12500,
            total_traffic: 85000,
            avg_position: 15.2,
            total_volume: 980000
          },
          {
            site_name: 'www.japan.travel',
            display_name: 'Japan Travel',
            total_keywords: 18900,
            total_traffic: 120000,
            avg_position: 12.8,
            total_volume: 1500000
          },
          {
            site_name: 'www.timeout.com/tokyo',
            display_name: 'Time Out Tokyo',
            total_keywords: 15200,
            total_traffic: 95000,
            avg_position: 18.5,
            total_volume: 1200000
          },
          {
            site_name: 'www.lonelyplanet.com/japan/tokyo',
            display_name: 'Lonely Planet Tokyo',
            total_keywords: 22100,
            total_traffic: 135000,
            avg_position: 14.3,
            total_volume: 1800000
          }
        ],
        summary: {
          total_competitors: 4,
          total_traffic: 435000,
          total_keywords: 68700
        }
      }
    case '/api/keywords/top-performing':
      return [
        {
          keyword: 'tokyo weekender',
          volume: 1400,
          organic_traffic: 1241,
          current_position: 1,
          keyword_difficulty: 2,
          current_url: 'https://www.tokyoweekender.com/'
        },
        {
          keyword: 'tokyo events',
          volume: 850,
          organic_traffic: 680,
          current_position: 3,
          keyword_difficulty: 15,
          current_url: 'https://www.tokyoweekender.com/events'
        },
        {
          keyword: 'tokyo restaurants',
          volume: 720,
          organic_traffic: 540,
          current_position: 5,
          keyword_difficulty: 25,
          current_url: 'https://www.tokyoweekender.com/restaurants'
        }
      ]
    case '/api/keywords/improvement-opportunities':
      return [
        {
          keyword: 'tokyo nightlife',
          volume: 650,
          organic_traffic: 195,
          current_position: 15,
          keyword_difficulty: 20,
          current_url: 'https://www.tokyoweekender.com/nightlife'
        },
        {
          keyword: 'tokyo shopping',
          volume: 580,
          organic_traffic: 174,
          current_position: 18,
          keyword_difficulty: 22,
          current_url: 'https://www.tokyoweekender.com/shopping'
        },
        {
          keyword: 'tokyo travel guide',
          volume: 520,
          organic_traffic: 156,
          current_position: 12,
          keyword_difficulty: 18,
          current_url: 'https://www.tokyoweekender.com/travel-guide'
        }
      ]
    case '/api/keywords/locations':
      return [
        {
          location: 'United States',
          keyword_count: 22387,
          total_traffic: 26958
        },
        {
          location: 'Australia',
          keyword_count: 4970,
          total_traffic: 4412
        },
        {
          location: 'Canada',
          keyword_count: 3870,
          total_traffic: 2515
        },
        {
          location: 'United Kingdom',
          keyword_count: 2939,
          total_traffic: 2971
        },
        {
          location: 'Philippines',
          keyword_count: 2779,
          total_traffic: 2539
        },
        {
          location: 'Japan',
          keyword_count: 2672,
          total_traffic: 8352
        },
        {
          location: 'India',
          keyword_count: 2021,
          total_traffic: 1756
        },
        {
          location: 'Singapore',
          keyword_count: 1709,
          total_traffic: 1711
        },
        {
          location: 'Indonesia',
          keyword_count: 1406,
          total_traffic: 964
        },
        {
          location: 'Malaysia',
          keyword_count: 1165,
          total_traffic: 975
        }
      ]
    case '/api/keywords/search':
      return [
        {
          Keyword: 'tokyo',
          'Country code': 'US',
          Location: 'United States',
          Volume: 252000,
          'Current position': 7,
          'Organic traffic': 558,
          KD: 84.0,
          'Current URL': 'https://www.tokyoweekender.com/entertainment/anime-and-manga/station-idol-latch-japan-anime-train-boys/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo travel guide',
          'Country code': 'US',
          Location: 'United States',
          Volume: 8500,
          'Current position': 3,
          'Organic traffic': 680,
          KD: 15,
          'Current URL': 'https://www.tokyoweekender.com/travel-guide/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo restaurants',
          'Country code': 'US',
          Location: 'United States',
          Volume: 7200,
          'Current position': 5,
          'Organic traffic': 540,
          KD: 25,
          'Current URL': 'https://www.tokyoweekender.com/restaurants',
          Informational: false,
          Commercial: true,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo nightlife',
          'Country code': 'US',
          Location: 'United States',
          Volume: 6500,
          'Current position': 15,
          'Organic traffic': 195,
          KD: 20,
          'Current URL': 'https://www.tokyoweekender.com/nightlife',
          Informational: false,
          Commercial: true,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo shopping',
          'Country code': 'US',
          Location: 'United States',
          Volume: 5800,
          'Current position': 18,
          'Organic traffic': 174,
          KD: 22,
          'Current URL': 'https://www.tokyoweekender.com/shopping',
          Informational: false,
          Commercial: true,
          Transactional: true,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo cherry blossom',
          'Country code': 'CA',
          Location: 'Canada',
          Volume: 12000,
          'Current position': 4,
          'Organic traffic': 850,
          KD: 18,
          'Current URL': 'https://www.tokyoweekender.com/seasonal/cherry-blossom/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo hotels',
          'Country code': 'CA',
          Location: 'Canada',
          Volume: 9500,
          'Current position': 8,
          'Organic traffic': 420,
          KD: 28,
          'Current URL': 'https://www.tokyoweekender.com/accommodation/',
          Informational: false,
          Commercial: true,
          Transactional: true,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo metro',
          'Country code': 'CA',
          Location: 'Canada',
          Volume: 7800,
          'Current position': 6,
          'Organic traffic': 380,
          KD: 12,
          'Current URL': 'https://www.tokyoweekender.com/transportation/metro/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo events',
          'Country code': 'AU',
          Location: 'Australia',
          Volume: 6800,
          'Current position': 2,
          'Organic traffic': 720,
          KD: 16,
          'Current URL': 'https://www.tokyoweekender.com/events',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo food',
          'Country code': 'AU',
          Location: 'Australia',
          Volume: 5500,
          'Current position': 9,
          'Organic traffic': 280,
          KD: 24,
          'Current URL': 'https://www.tokyoweekender.com/food/',
          Informational: false,
          Commercial: true,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo ramen',
          'Country code': 'AU',
          Location: 'Australia',
          Volume: 4200,
          'Current position': 12,
          'Organic traffic': 180,
          KD: 19,
          'Current URL': 'https://www.tokyoweekender.com/food/ramen/',
          Informational: false,
          Commercial: true,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo temples',
          'Country code': 'GB',
          Location: 'United Kingdom',
          Volume: 3800,
          'Current position': 7,
          'Organic traffic': 220,
          KD: 14,
          'Current URL': 'https://www.tokyoweekender.com/culture/temples/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo museums',
          'Country code': 'GB',
          Location: 'United Kingdom',
          Volume: 3200,
          'Current position': 11,
          'Organic traffic': 150,
          KD: 17,
          'Current URL': 'https://www.tokyoweekender.com/culture/museums/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo anime',
          'Country code': 'GB',
          Location: 'United Kingdom',
          Volume: 2800,
          'Current position': 14,
          'Organic traffic': 120,
          KD: 21,
          'Current URL': 'https://www.tokyoweekender.com/entertainment/anime/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo weather',
          'Country code': 'JP',
          Location: 'Japan',
          Volume: 15000,
          'Current position': 1,
          'Organic traffic': 1200,
          KD: 8,
          'Current URL': 'https://www.tokyoweekender.com/weather/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo station',
          'Country code': 'JP',
          Location: 'Japan',
          Volume: 12000,
          'Current position': 2,
          'Organic traffic': 950,
          KD: 10,
          'Current URL': 'https://www.tokyoweekender.com/transportation/station/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo airport',
          'Country code': 'JP',
          Location: 'Japan',
          Volume: 9800,
          'Current position': 3,
          'Organic traffic': 780,
          KD: 13,
          'Current URL': 'https://www.tokyoweekender.com/transportation/airport/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo sushi',
          'Country code': 'JP',
          Location: 'Japan',
          Volume: 8500,
          'Current position': 5,
          'Organic traffic': 650,
          KD: 20,
          'Current URL': 'https://www.tokyoweekender.com/food/sushi/',
          Informational: false,
          Commercial: true,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo bars',
          'Country code': 'JP',
          Location: 'Japan',
          Volume: 7200,
          'Current position': 8,
          'Organic traffic': 420,
          KD: 23,
          'Current URL': 'https://www.tokyoweekender.com/nightlife/bars/',
          Informational: false,
          Commercial: true,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'tokyo parks',
          'Country code': 'JP',
          Location: 'Japan',
          Volume: 6500,
          'Current position': 6,
          'Organic traffic': 380,
          KD: 15,
          'Current URL': 'https://www.tokyoweekender.com/attractions/parks/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'omoide yokocho',
          'Country code': 'US',
          Location: 'Japan',
          Volume: 12000,
          'Current position': 28,
          'Organic traffic': 4,
          KD: 3.0,
          'Current URL': 'https://www.tokyoweekender.com/things-to-do-in-tokyo/the-most-instagram-worthy-spots-in-tokyo-without-the-crowds/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: true
        },
        {
          Keyword: 'saori araki',
          'Country code': 'US',
          Location: 'Japan',
          Volume: 12000,
          'Current position': 9,
          'Organic traffic': 369,
          KD: 0.0,
          'Current URL': 'https://www.tokyoweekender.com/entertainment/saori-araki-the-japanese-salarywoman-breaking-the-internet/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        },
        {
          Keyword: 'pisces horoscope',
          'Country code': 'AU',
          Location: 'Japan',
          Volume: 8800,
          'Current position': 2,
          'Organic traffic': 473,
          KD: 26.0,
          'Current URL': 'https://www.tokyoweekender.com/entertainment/your-october-2025-horoscope/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        },
        {
          Keyword: 'respect for the aged day',
          'Country code': 'JP',
          Location: 'Japan',
          Volume: 8700,
          'Current position': 13,
          'Organic traffic': 59,
          KD: 1.0,
          'Current URL': 'https://www.tokyoweekender.com/art_and_culture/japanese-culture/japanese-holidays-what-is-keiro-no-hi-respect-for-the-aged-day/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        },
        {
          Keyword: 'junko furuta',
          'Country code': 'ID',
          Location: 'Japan',
          Volume: 7900,
          'Current position': 9,
          'Organic traffic': 17,
          KD: 0.0,
          'Current URL': 'https://www.tokyoweekender.com/japan-life/news-and-opinion/junko-furuta-murder-case-justice-revisited/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        },
        {
          Keyword: 'tofu kya hota hai',
          'Country code': 'IN',
          Location: 'Japan',
          Volume: 7400,
          'Current position': 44,
          'Organic traffic': 0,
          KD: 2.0,
          'Current URL': 'https://www.tokyoweekender.com/food-and-drink/what-is-tofu/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        },
        {
          Keyword: 'princess mako',
          'Country code': 'GB',
          Location: 'Japan',
          Volume: 7100,
          'Current position': 9,
          'Organic traffic': 0,
          KD: 3.0,
          'Current URL': 'https://www.tokyoweekender.com/art_and_culture/list-7-things-know-princess-mako/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        },
        {
          Keyword: 'junko furuta',
          'Country code': 'TR',
          Location: 'Japan',
          Volume: 6900,
          'Current position': 39,
          'Organic traffic': 0,
          KD: 0.0,
          'Current URL': 'https://www.tokyoweekender.com/japan-life/news-and-opinion/junko-furuta-murder-case-justice-revisited/',
          Informational: true,
          Commercial: false,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        },
        {
          Keyword: 'nobita shizuka',
          'Country code': 'IN',
          Location: 'Japan',
          Volume: 6800,
          'Current position': 42,
          'Organic traffic': 0,
          KD: 0.0,
          'Current URL': 'https://www.tokyoweekender.com/entertainment/anime-and-manga/takopis-original-sin-the-dark-doraemon/',
          Informational: true,
          Commercial: true,
          Transactional: false,
          Navigational: false,
          Branded: false,
          Local: false
        }
      ]
    case '/api/competitors/tokyocheapo.com/comparison':
    case '/api/competitors/www.japan.travel/comparison':
    case '/api/competitors/www.timeout.com/tokyo/comparison':
    case '/api/competitors/www.lonelyplanet.com/japan/tokyo/comparison':
      return [
        {
          keyword: 'tokyo restaurants',
          volume: 720,
          competitor_position: 3,
          competitor_traffic: 450,
          competitor_url: 'https://tokyocheapo.com/restaurants/',
          keyword_difficulty: 25,
          cpc: 1.2,
          serp_features: 'Local Pack',
          informational: false,
          commercial: true,
          transactional: false,
          navigational: false,
          branded: false,
          local: true,
          tokyo_weekender_position: 5,
          tokyo_weekender_traffic: 540,
          tokyo_weekender_url: 'https://www.tokyoweekender.com/restaurants',
          opportunity_score: 85,
          status: 'worse'
        },
        {
          keyword: 'tokyo events',
          volume: 850,
          competitor_position: 2,
          competitor_traffic: 680,
          competitor_url: 'https://tokyocheapo.com/events/',
          keyword_difficulty: 15,
          cpc: 0.8,
          serp_features: 'Featured Snippets',
          informational: true,
          commercial: false,
          transactional: false,
          navigational: false,
          branded: false,
          local: true,
          tokyo_weekender_position: 3,
          tokyo_weekender_traffic: 680,
          tokyo_weekender_url: 'https://www.tokyoweekender.com/events',
          opportunity_score: 75,
          status: 'worse'
        },
        {
          keyword: 'tokyo nightlife',
          volume: 650,
          competitor_position: 1,
          competitor_traffic: 520,
          competitor_url: 'https://tokyocheapo.com/nightlife/',
          keyword_difficulty: 20,
          cpc: 1.5,
          serp_features: 'Image Pack',
          informational: false,
          commercial: true,
          transactional: false,
          navigational: false,
          branded: false,
          local: true,
          tokyo_weekender_position: 15,
          tokyo_weekender_traffic: 195,
          tokyo_weekender_url: 'https://www.tokyoweekender.com/nightlife',
          opportunity_score: 95,
          status: 'worse'
        },
        {
          keyword: 'tokyo shopping',
          volume: 580,
          competitor_position: 4,
          competitor_traffic: 290,
          competitor_url: 'https://tokyocheapo.com/shopping/',
          keyword_difficulty: 18,
          cpc: 1.0,
          serp_features: 'Local Pack',
          informational: false,
          commercial: true,
          transactional: true,
          navigational: false,
          branded: false,
          local: true,
          tokyo_weekender_position: 18,
          tokyo_weekender_traffic: 174,
          tokyo_weekender_url: 'https://www.tokyoweekender.com/shopping',
          opportunity_score: 90,
          status: 'worse'
        },
        {
          keyword: 'tokyo travel guide',
          volume: 420,
          competitor_position: 2,
          competitor_traffic: 336,
          competitor_url: 'https://tokyocheapo.com/travel-guide/',
          keyword_difficulty: 12,
          cpc: 0.6,
          serp_features: 'Featured Snippets',
          informational: true,
          commercial: false,
          transactional: false,
          navigational: false,
          branded: false,
          local: true,
          tokyo_weekender_position: 8,
          tokyo_weekender_traffic: 252,
          tokyo_weekender_url: 'https://www.tokyoweekender.com/guide',
          opportunity_score: 70,
          status: 'worse'
        }
      ]
    case '/api/content/recommendations':
      return {
        summary: {
          new_content_proposals: 8,
          improvement_proposals: 12,
          potential_traffic: 45000,
          priority: 'High'
        },
        new_content: [
          {
            title: 'Tokyo Cherry Blossom Viewing Spots 2024',
            keyword: 'tokyo cherry blossom spots',
            volume: 3200,
            difficulty: 15,
            potential_traffic: 8500,
            content_type: 'Guide',
            priority: 'High',
            estimated_effort: 'Medium',
            target_audience: 'Tourists',
            content_angle: 'Seasonal guide with best viewing times and locations'
          },
          {
            title: 'Best Tokyo Ramen Shops by District',
            keyword: 'best tokyo ramen shops',
            volume: 2800,
            difficulty: 22,
            potential_traffic: 7200,
            content_type: 'Listicle',
            priority: 'High',
            estimated_effort: 'High',
            target_audience: 'Food enthusiasts',
            content_angle: 'Comprehensive district-by-district ramen guide'
          },
          {
            title: 'Tokyo Day Trip Destinations from Central Tokyo',
            keyword: 'tokyo day trips',
            volume: 2100,
            difficulty: 18,
            potential_traffic: 5600,
            content_type: 'Guide',
            priority: 'Medium',
            estimated_effort: 'Medium',
            target_audience: 'Tourists',
            content_angle: 'Accessible day trip options with transport details'
          },
          {
            title: 'Tokyo Nightlife Districts Complete Guide',
            keyword: 'tokyo nightlife districts',
            volume: 1800,
            difficulty: 25,
            potential_traffic: 4800,
            content_type: 'Guide',
            priority: 'Medium',
            estimated_effort: 'High',
            target_audience: 'Young adults',
            content_angle: 'Comprehensive nightlife area comparison'
          }
        ],
        improvements: [
          {
            title: 'Tokyo Events Calendar',
            current_url: 'https://www.tokyoweekender.com/events',
            keyword: 'tokyo events',
            current_position: 3,
            target_position: 1,
            potential_traffic_gain: 1200,
            improvement_type: 'Content Enhancement',
            priority: 'High',
            recommendations: [
              'Add more detailed event descriptions',
              'Include event photos and videos',
              'Add user reviews and ratings',
              'Implement event filtering by category'
            ]
          },
          {
            title: 'Tokyo Restaurants Guide',
            current_url: 'https://www.tokyoweekender.com/restaurants',
            keyword: 'tokyo restaurants',
            current_position: 5,
            target_position: 2,
            potential_traffic_gain: 800,
            improvement_type: 'SEO Optimization',
            priority: 'High',
            recommendations: [
              'Optimize meta descriptions',
              'Add structured data markup',
              'Improve page loading speed',
              'Add more restaurant photos'
            ]
          },
          {
            title: 'Tokyo Shopping Areas',
            current_url: 'https://www.tokyoweekender.com/shopping',
            keyword: 'tokyo shopping',
            current_position: 18,
            target_position: 8,
            potential_traffic_gain: 1500,
            improvement_type: 'Content Expansion',
            priority: 'Medium',
            recommendations: [
              'Add shopping district maps',
              'Include store opening hours',
              'Add price range information',
              'Create shopping itinerary suggestions'
            ]
          }
        ],
        topic_clusters: [
          {
            cluster_name: 'Tokyo Food & Dining',
            primary_keyword: 'tokyo food',
            supporting_keywords: [
              'tokyo ramen',
              'tokyo sushi',
              'tokyo street food',
              'tokyo izakaya',
              'tokyo dessert'
            ],
            content_pieces: 6,
            potential_traffic: 25000,
            priority: 'High'
          },
          {
            cluster_name: 'Tokyo Transportation',
            primary_keyword: 'tokyo transportation',
            supporting_keywords: [
              'tokyo metro',
              'tokyo train',
              'tokyo bus',
              'tokyo taxi',
              'tokyo airport transfer'
            ],
            content_pieces: 5,
            potential_traffic: 18000,
            priority: 'Medium'
          },
          {
            cluster_name: 'Tokyo Accommodation',
            primary_keyword: 'tokyo hotels',
            supporting_keywords: [
              'tokyo ryokan',
              'tokyo capsule hotel',
              'tokyo budget accommodation',
              'tokyo luxury hotels',
              'tokyo business hotels'
            ],
            content_pieces: 4,
            potential_traffic: 22000,
            priority: 'High'
          }
        ]
      }
    default:
      return {}
  }
}

export const apiRequest = async (endpoint: string, _options?: RequestInit): Promise<Response> => {
  // Temporarily use mock data for all endpoints until backend is fixed
  console.log(`Using mock data for ${endpoint} (backend temporarily disabled)`)
  
  let mockData = getMockData(endpoint)
  
  // Apply dynamic filtering for search endpoint
  if (endpoint.startsWith('/api/keywords/search')) {
    const url = new URL(endpoint, 'http://localhost')
    const minVolume = parseInt(url.searchParams.get('min_volume') || '100')
    const maxPosition = parseInt(url.searchParams.get('max_position') || '50')
    const intent = url.searchParams.get('intent') || ''
    const location = url.searchParams.get('location') || ''
    const limit = parseInt(url.searchParams.get('limit') || '100')
    
    console.log(`Applying filters: min_volume=${minVolume}, max_position=${maxPosition}, intent=${intent}, location=${location}, limit=${limit}`)
    
    // Filter the mock data
    mockData = mockData.filter((item: any) => {
      // Volume filter
      if (item.Volume < minVolume) return false
      
      // Position filter
      if (item['Current position'] > maxPosition) return false
      
      // Intent filter
      if (intent && item[intent] !== true) return false
      
      // Location filter
      if (location && item.Location !== location) return false
      
      return true
    })
    
    // Sort by traffic and position
    mockData.sort((a: any, b: any) => {
      if (b['Organic traffic'] !== a['Organic traffic']) {
        return b['Organic traffic'] - a['Organic traffic']
      }
      return a['Current position'] - b['Current position']
    })
    
    // Apply limit
    mockData = mockData.slice(0, limit)
    
    console.log(`Filtered results: ${mockData.length} items`)
  }
  
  console.log(`Mock data for ${endpoint}:`, mockData)
  
  // Simulate network delay for realistic behavior
  await new Promise(resolve => setTimeout(resolve, 100))
  
  return new Response(JSON.stringify(mockData), {
    status: 200,
    statusText: 'OK',
    headers: {
      'Content-Type': 'application/json',
    },
  })
}

// Create and export axios instance
export const api = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
})

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data)
    } else if (error.request) {
      // Request made but no response received
      console.error('Network Error:', error.message)
    } else {
      // Error in request configuration
      console.error('Request Error:', error.message)
    }
    return Promise.reject(error)
  }
)
