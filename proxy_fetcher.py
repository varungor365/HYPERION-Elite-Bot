"""
Automatic Proxy Fetcher with AI Quality Checker
Fetches free proxies from multiple providers via their APIs
AI-powered quality assessment and filtering
"""

import requests
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import time
import json
import concurrent.futures
from datetime import datetime
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import plugin manager for dynamic proxy sources
try:
    from plugin_manager import plugin_manager
    PLUGIN_MANAGER_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ Plugin manager not available, using fallback sources")
    PLUGIN_MANAGER_AVAILABLE = False


@dataclass
class ProxySource:
    """Information about a proxy source"""
    name: str
    url: str
    parser: str  # Method to use for parsing
    timeout: int = 10
    enabled: bool = True


@dataclass
class ProxyQuality:
    """AI-assessed proxy quality metrics"""
    proxy: str
    speed_ms: float
    success_rate: float
    stability_score: float
    anonymity_level: str  # 'transparent', 'anonymous', 'elite'
    quality_score: float  # 0-100 AI calculated score
    location: str = "Unknown"
    test_time: float = field(default_factory=time.time)
    
    def get_grade(self) -> str:
        """Get letter grade based on quality score"""
        if self.quality_score >= 90:
            return "A+ (Elite)"
        elif self.quality_score >= 80:
            return "A (Excellent)"
        elif self.quality_score >= 70:
            return "B (Good)"
        elif self.quality_score >= 60:
            return "C (Average)"
        elif self.quality_score >= 50:
            return "D (Poor)"
        else:
            return "F (Bad)"


class AIProxyChecker:
    """AI-powered proxy quality assessment system with MEGA-specific testing"""
    
    def __init__(self):
        self.test_urls = [
            'https://httpbin.org/ip',
            'https://api.ipify.org?format=json',
            'https://ifconfig.me/all.json'
        ]
        self.mega_test_url = 'https://g.api.mega.co.nz/cs'  # MEGA API endpoint
        self.anonymity_test_url = 'https://httpbin.org/headers'
        
    def test_mega_compatibility(self, proxy: str, timeout: int = 10) -> Tuple[bool, str]:
        """
        Test if proxy works with MEGA specifically
        
        Returns:
            (is_working, reason)
        """
        try:
            # Test 1: Can reach MEGA API
            start_time = time.time()
            response = requests.post(
                self.mega_test_url,
                json=[{"a": "g", "v": 3}],  # Simple MEGA API request
                proxies={'http': proxy, 'https': proxy},
                timeout=timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Content-Type': 'application/json'
                }
            )
            elapsed = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                # Check if response looks like MEGA API response
                try:
                    data = response.json()
                    if isinstance(data, list):
                        return (True, f"MEGA OK ({elapsed:.0f}ms)")
                except:
                    pass
            
            # Test 2: Check if blocked by MEGA
            if response.status_code == 403:
                return (False, "Blocked by MEGA (403)")
            elif response.status_code == 429:
                return (False, "Rate limited by MEGA")
            elif response.status_code >= 500:
                return (False, "MEGA server error")
            else:
                return (False, f"Invalid response ({response.status_code})")
                
        except requests.exceptions.Timeout:
            return (False, "Timeout (too slow)")
        except requests.exceptions.ProxyError:
            return (False, "Proxy connection failed")
        except requests.exceptions.SSLError:
            return (False, "SSL error")
        except requests.exceptions.ConnectionError:
            return (False, "Connection refused")
        except Exception as e:
            return (False, f"Error: {str(e)[:30]}")
    
    def analyze_proxy(self, proxy: str, timeout: int = 10) -> Optional[ProxyQuality]:
        """
        AI-powered comprehensive proxy analysis with MEGA testing
        
        Tests:
        - Speed (response time)
        - Success rate (multiple requests)
        - Stability (consistency)
        - Anonymity level
        - MEGA compatibility (critical)
        """
        try:
            # CRITICAL: Test MEGA compatibility first
            mega_ok, mega_reason = self.test_mega_compatibility(proxy, timeout)
            
            if not mega_ok:
                logger.debug(f"✗ {proxy[:30]:30} | MEGA: {mega_reason}")
                return None  # Reject if doesn't work with MEGA
            
            speeds = []
            successes = 0
            total_tests = 3
            
            # Test speed and reliability with general endpoints
            for i, test_url in enumerate(self.test_urls[:total_tests]):
                try:
                    start_time = time.time()
                    response = requests.get(
                        test_url,
                        proxies={'http': proxy, 'https': proxy},
                        timeout=timeout,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    )
                    elapsed = (time.time() - start_time) * 1000  # Convert to ms
                    
                    if response.status_code == 200:
                        speeds.append(elapsed)
                        successes += 1
                    
                    # Small delay between tests
                    if i < total_tests - 1:
                        time.sleep(0.3)
                        
                except:
                    continue
            
            if not speeds or successes == 0:
                return None
            
            # Calculate metrics
            avg_speed = statistics.mean(speeds)
            success_rate = (successes / total_tests) * 100
            
            # Stability score (lower variance = higher stability)
            if len(speeds) > 1:
                speed_variance = statistics.stdev(speeds)
                stability = max(0, 100 - (speed_variance / avg_speed * 100))
            else:
                stability = 50  # Single test, assume medium stability
            
            # Check anonymity level
            anonymity = self._check_anonymity(proxy, timeout)
            
            # AI Quality Score Calculation (MEGA compatibility is already verified)
            quality_score = self._calculate_ai_quality_score(
                avg_speed, success_rate, stability, anonymity
            )
            
            # Bonus points for MEGA compatibility
            quality_score = min(100, quality_score + 10)  # +10 bonus for MEGA working
            
            return ProxyQuality(
                proxy=proxy,
                speed_ms=round(avg_speed, 2),
                success_rate=round(success_rate, 2),
                stability_score=round(stability, 2),
                anonymity_level=anonymity,
                quality_score=round(quality_score, 2),
                location=mega_reason  # Store MEGA test result
            )
            
        except Exception as e:
            logger.debug(f"Error analyzing proxy {proxy}: {e}")
            return None
    
    def _check_anonymity(self, proxy: str, timeout: int = 5) -> str:
        """Check proxy anonymity level"""
        try:
            response = requests.get(
                self.anonymity_test_url,
                proxies={'http': proxy, 'https': proxy},
                timeout=timeout
            )
            
            if response.status_code == 200:
                headers = response.json().get('headers', {})
                
                # Check for revealing headers
                if 'X-Forwarded-For' in headers or 'Via' in headers:
                    return 'transparent'
                elif 'X-Real-Ip' in headers:
                    return 'anonymous'
                else:
                    return 'elite'
            
            return 'anonymous'
            
        except:
            return 'unknown'
    
    def _calculate_ai_quality_score(self, speed: float, success_rate: float, 
                                     stability: float, anonymity: str) -> float:
        """
        AI-powered quality score calculation
        
        Weights:
        - Speed: 30%
        - Success Rate: 35%
        - Stability: 25%
        - Anonymity: 10%
        """
        # Speed score (faster = better, logarithmic scale)
        if speed < 500:
            speed_score = 100
        elif speed < 1000:
            speed_score = 90 - (speed - 500) / 500 * 40
        elif speed < 2000:
            speed_score = 50 - (speed - 1000) / 1000 * 30
        elif speed < 5000:
            speed_score = 20 - (speed - 2000) / 3000 * 20
        else:
            speed_score = max(0, 10 - (speed - 5000) / 5000 * 10)
        
        # Anonymity score
        anonymity_scores = {
            'elite': 100,
            'anonymous': 70,
            'transparent': 30,
            'unknown': 50
        }
        anonymity_score = anonymity_scores.get(anonymity, 50)
        
        # Weighted calculation
        quality = (
            speed_score * 0.30 +
            success_rate * 0.35 +
            stability * 0.25 +
            anonymity_score * 0.10
        )
        
        return min(100, max(0, quality))
    
    def batch_analyze(self, proxies: List[str], max_workers: int = 10, 
                     timeout: int = 10) -> List[ProxyQuality]:
        """
        Analyze multiple proxies in parallel using AI
        
        Args:
            proxies: List of proxy URLs
            max_workers: Number of parallel workers
            timeout: Timeout per proxy test
            
        Returns:
            List of ProxyQuality objects (only successful)
        """
        results = []
        total = len(proxies)
        
        logger.info(f"🤖 AI analyzing {total} proxies (using {max_workers} workers)...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_proxy = {
                executor.submit(self.analyze_proxy, proxy, timeout): proxy 
                for proxy in proxies
            }
            
            # Collect results as they complete
            completed = 0
            for future in concurrent.futures.as_completed(future_to_proxy):
                completed += 1
                proxy = future_to_proxy[future]
                
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        logger.info(
                            f"✓ [{completed}/{total}] {proxy[:30]:30} | "
                            f"Speed: {result.speed_ms:>6.0f}ms | "
                            f"Score: {result.quality_score:>5.1f}/100 | "
                            f"Grade: {result.get_grade()}"
                        )
                    else:
                        logger.debug(f"✗ [{completed}/{total}] {proxy[:30]:30} | Failed")
                except Exception as e:
                    logger.debug(f"✗ [{completed}/{total}] {proxy[:30]:30} | Error: {e}")
        
        # Sort by quality score (best first)
        results.sort(key=lambda x: x.quality_score, reverse=True)
        
        logger.info(f"🎯 AI found {len(results)} working proxies out of {total}")
        
        return results
    
    def filter_by_quality(self, qualities: List[ProxyQuality], 
                         min_score: float = 60) -> List[ProxyQuality]:
        """Filter proxies by minimum quality score"""
        filtered = [q for q in qualities if q.quality_score >= min_score]
        logger.info(f"📊 Filtered to {len(filtered)} proxies with score >= {min_score}")
        return filtered
    
    def get_best_proxies(self, qualities: List[ProxyQuality], 
                        count: int = 20) -> List[str]:
        """Get the best N proxies by quality score"""
        sorted_qualities = sorted(qualities, key=lambda x: x.quality_score, reverse=True)
        best = sorted_qualities[:count]
        
        logger.info(f"🏆 Top {len(best)} proxies selected (scores: {best[0].quality_score:.1f} - {best[-1].quality_score:.1f})")
        
        return [q.proxy for q in best]
    
    def generate_report(self, qualities: List[ProxyQuality]) -> str:
        """Generate AI quality report"""
        if not qualities:
            return "No proxies analyzed"
        
        avg_score = statistics.mean([q.quality_score for q in qualities])
        avg_speed = statistics.mean([q.speed_ms for q in qualities])
        avg_success = statistics.mean([q.success_rate for q in qualities])
        
        # Grade distribution
        grades = [q.get_grade() for q in qualities]
        grade_counts = {}
        for grade in grades:
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        report = "\n" + "="*70 + "\n"
        report += "🤖 AI PROXY QUALITY REPORT\n"
        report += "="*70 + "\n\n"
        report += f"Total Analyzed: {len(qualities)}\n"
        report += f"Average Quality Score: {avg_score:.2f}/100\n"
        report += f"Average Speed: {avg_speed:.0f}ms\n"
        report += f"Average Success Rate: {avg_success:.1f}%\n\n"
        report += "Grade Distribution:\n"
        for grade, count in sorted(grade_counts.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * (count * 40 // len(qualities))
            report += f"  {grade:20} {bar} {count}\n"
        report += "\n"
        report += "Top 5 Proxies:\n"
        for i, q in enumerate(qualities[:5], 1):
            report += f"  {i}. {q.proxy[:40]:40} | Score: {q.quality_score:>5.1f} | Speed: {q.speed_ms:>6.0f}ms | {q.get_grade()}\n"
        report += "="*70 + "\n"
        
        return report


class ProxyFetcher:
    """Fetches proxies from multiple free API sources with AI quality checking"""
    
    def __init__(self):
        self.sources = {
            # ProxyScrape - Reliable and well-maintained
            'proxyscrape_http': ProxySource(
                name='ProxyScrape HTTP',
                url='https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&timeout=10000',
                parser='text_list',
                enabled=True
            ),
            'proxyscrape_socks5': ProxySource(
                name='ProxyScrape SOCKS5',
                url='https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=socks5&proxy_format=protocolipport&format=text&timeout=10000',
                parser='text_list',
                enabled=True
            ),
            # GitHub proxy lists - Frequently updated
            'proxifly': ProxySource(
                name='Proxifly GitHub',
                url='https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt',
                parser='text_list_plain',
                enabled=True
            ),
            'monosans_http': ProxySource(
                name='Monosans HTTP',
                url='https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
                parser='text_list_plain',
                enabled=True
            ),
            'monosans_socks5': ProxySource(
                name='Monosans SOCKS5',
                url='https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
                parser='text_list_plain',
                enabled=True
            ),
            'speedx_http': ProxySource(
                name='SpeedX HTTP',
                url='https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
                parser='text_list_plain',
                enabled=True
            ),
            'speedx_socks5': ProxySource(
                name='SpeedX SOCKS5',
                url='https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
                parser='text_list_plain',
                enabled=True
            ),
            # Clarketm - Large collection
            'clarketm_http': ProxySource(
                name='Clarketm HTTP',
                url='https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
                parser='text_list_plain',
                enabled=True
            ),
            # GeoNode - API with fresh proxies
            'geonode': ProxySource(
                name='GeoNode API',
                url='https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc&protocols=http%2Chttps',
                parser='geonode',
                enabled=True
            ),
            # Proxy11 - GitHub list
            'proxy11': ProxySource(
                name='Proxy11 GitHub',
                url='https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
                parser='text_list_plain',
                enabled=True
            ),
            # Jetkai - Comprehensive list
            'jetkai_http': ProxySource(
                name='Jetkai HTTP',
                url='https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
                parser='text_list_plain',
                enabled=True
            ),
            'jetkai_https': ProxySource(
                name='Jetkai HTTPS',
                url='https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
                parser='text_list_plain',
                enabled=True
            ),
            # ShiftyTR - Active list
            'shiftytr': ProxySource(
                name='ShiftyTR GitHub',
                url='https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
                parser='text_list_plain',
                enabled=True
            ),
            # HookZof - Verified proxies
            'hookzof': ProxySource(
                name='HookZof Verified',
                url='https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
                parser='text_list_plain',
                enabled=True
            ),
            # MuRongPIG - Chinese mirror but global proxies
            'murongpig': ProxySource(
                name='MuRongPIG List',
                url='https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
                parser='text_list_plain',
                enabled=True
            )
        }
        
        self.fetched_proxies: List[str] = []
        self.last_fetch_time: Optional[float] = None
        self.fetch_interval = 300  # 5 minutes between fetches
        self.ai_checker = AIProxyChecker()  # AI quality checker
    
    def fetch_all_sources(self, max_proxies: int = 100) -> List[str]:
        """
        Fetch proxies from all enabled sources
        
        Args:
            max_proxies: Maximum number of proxies to return
            
        Returns:
            List of proxy URLs
        """
        all_proxies = []
        
        for source_name, source in self.sources.items():
            if not source.enabled:
                continue
            
            try:
                logger.info(f"📡 Fetching proxies from {source.name}...")
                proxies = self._fetch_from_source(source)
                
                if proxies:
                    all_proxies.extend(proxies)
                    logger.info(f"✅ Got {len(proxies)} proxies from {source.name}")
                else:
                    logger.warning(f"⚠️ No proxies from {source.name}")
                
                # Small delay between sources to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Error fetching from {source.name}: {e}")
                continue
        
        # Remove duplicates
        unique_proxies = list(set(all_proxies))
        logger.info(f"🎯 Total unique proxies fetched: {len(unique_proxies)}")
        
        # Limit to max_proxies
        self.fetched_proxies = unique_proxies[:max_proxies]
        self.last_fetch_time = time.time()
        
        return self.fetched_proxies
    
    def fetch_high_quality(self, max_proxies: int = 50, min_quality_score: float = 70,
                          test_sample_size: int = 200, max_workers: int = 20) -> List[str]:
        """
        Fetch and AI-test proxies, returning only high-quality ones
        
        Args:
            max_proxies: Maximum number of high-quality proxies to return
            min_quality_score: Minimum AI quality score (0-100)
            test_sample_size: Number of proxies to test
            max_workers: Parallel workers for testing
            
        Returns:
            List of high-quality proxy URLs
        """
        logger.info("🚀 Starting AI-powered high-quality proxy fetch...")
        
        # Step 1: Fetch raw proxies
        logger.info("📡 Step 1: Fetching proxies from all sources...")
        raw_proxies = self.fetch_all_sources(max_proxies=test_sample_size * 2)
        
        if not raw_proxies:
            logger.error("❌ Failed to fetch any proxies")
            return []
        
        # Step 2: AI quality testing (sample)
        logger.info(f"🤖 Step 2: AI analyzing top {min(test_sample_size, len(raw_proxies))} proxies...")
        test_proxies = raw_proxies[:test_sample_size]
        
        qualities = self.ai_checker.batch_analyze(
            test_proxies,
            max_workers=max_workers,
            timeout=8
        )
        
        if not qualities:
            logger.warning("⚠️ No proxies passed AI quality tests")
            return []
        
        # Step 3: Filter by quality
        logger.info(f"📊 Step 3: Filtering proxies with score >= {min_quality_score}...")
        high_quality = self.ai_checker.filter_by_quality(qualities, min_quality_score)
        
        if not high_quality:
            logger.warning(f"⚠️ No proxies meet quality threshold of {min_quality_score}")
            # Lower threshold and retry
            min_quality_score = 50
            logger.info(f"🔄 Retrying with lower threshold: {min_quality_score}...")
            high_quality = self.ai_checker.filter_by_quality(qualities, min_quality_score)
        
        # Step 4: Get best proxies
        best_proxies = self.ai_checker.get_best_proxies(high_quality, max_proxies)
        
        # Step 5: Generate report
        print(self.ai_checker.generate_report(high_quality))
        
        logger.info(f"✅ Successfully selected {len(best_proxies)} high-quality proxies")
        
        self.fetched_proxies = best_proxies
        self.last_fetch_time = time.time()
        
        return best_proxies
    
    def _fetch_from_source(self, source: ProxySource) -> List[str]:
        """
        Fetch proxies from a single source
        
        Args:
            source: ProxySource configuration
            
        Returns:
            List of proxy URLs
        """
        try:
            response = requests.get(
                source.url,
                timeout=source.timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response.raise_for_status()
            
            # Parse based on format
            if source.parser == 'text_list':
                return self._parse_text_list(response.text, with_protocol=True)
            elif source.parser == 'text_list_plain':
                return self._parse_text_list_plain(response.text)
            elif source.parser == 'geonode':
                return self._parse_geonode(response.text)
            else:
                logger.warning(f"Unknown parser: {source.parser}")
                return []
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching from {source.name}")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error from {source.name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing {source.name}: {e}")
            return []
    
    def _parse_text_list(self, text: str, with_protocol: bool = False) -> List[str]:
        """Parse simple text list of proxies (one per line)"""
        proxies = []
        for line in text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                if with_protocol:
                    proxies.append(line)
                else:
                    # Assume http if no protocol
                    if '://' not in line:
                        proxies.append(f'http://{line}')
                    else:
                        proxies.append(line)
        return proxies
    
    def _parse_text_list_plain(self, text: str) -> List[str]:
        """Parse plain IP:PORT list and add http:// prefix"""
        proxies = []
        for line in text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Check if it's IP:PORT format
                if ':' in line and '://' not in line:
                    # Add http:// prefix
                    proxies.append(f'http://{line}')
                elif '://' in line:
                    proxies.append(line)
        return proxies
    
    def _parse_geonode(self, text: str) -> List[str]:
        """Parse GeoNode API response"""
        try:
            data = json.loads(text)
            proxies = []
            
            if 'data' in data:
                for proxy in data['data']:
                    ip = proxy.get('ip')
                    port = proxy.get('port')
                    protocols = proxy.get('protocols', ['http'])
                    
                    if ip and port:
                        # Use first protocol
                        protocol = protocols[0] if protocols else 'http'
                        proxies.append(f'{protocol}://{ip}:{port}')
            
            return proxies
        except json.JSONDecodeError:
            logger.error("Invalid JSON from GeoNode")
            return []
    
    def save_to_file(self, filepath: str, proxies: Optional[List[str]] = None) -> int:
        """
        Save fetched proxies to file
        
        Args:
            filepath: Path to save proxies
            proxies: List of proxies (uses self.fetched_proxies if None)
            
        Returns:
            Number of proxies saved
        """
        proxies_to_save = proxies if proxies is not None else self.fetched_proxies
        
        if not proxies_to_save:
            logger.warning("No proxies to save")
            return 0
        
        try:
            with open(filepath, 'w') as f:
                f.write("# Auto-fetched free proxies\n")
                f.write(f"# Fetched at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total proxies: {len(proxies_to_save)}\n\n")
                
                for proxy in proxies_to_save:
                    f.write(f"{proxy}\n")
            
            logger.info(f"✅ Saved {len(proxies_to_save)} proxies to {filepath}")
            return len(proxies_to_save)
            
        except Exception as e:
            logger.error(f"Error saving proxies to file: {e}")
            return 0
    
    def fetch_and_test(self, test_url: str = 'https://httpbin.org/ip', max_proxies: int = 50) -> List[str]:
        """
        Fetch proxies and test them
        
        Args:
            test_url: URL to test proxies against
            max_proxies: Maximum number of working proxies to return
            
        Returns:
            List of working proxy URLs
        """
        logger.info("🔄 Fetching proxies from all sources...")
        all_proxies = self.fetch_all_sources(max_proxies=200)
        
        if not all_proxies:
            logger.error("❌ No proxies fetched from any source")
            return []
        
        logger.info(f"🧪 Testing {len(all_proxies)} proxies (this may take a while)...")
        working_proxies = []
        
        for i, proxy in enumerate(all_proxies, 1):
            if len(working_proxies) >= max_proxies:
                break
            
            try:
                response = requests.get(
                    test_url,
                    proxies={'http': proxy, 'https': proxy},
                    timeout=5
                )
                
                if response.status_code == 200:
                    working_proxies.append(proxy)
                    logger.info(f"✅ [{i}/{len(all_proxies)}] Working: {proxy}")
                else:
                    logger.debug(f"❌ [{i}/{len(all_proxies)}] Failed: {proxy}")
                    
            except Exception as e:
                logger.debug(f"❌ [{i}/{len(all_proxies)}] Error: {proxy} - {str(e)[:50]}")
                continue
            
            # Small delay to avoid overwhelming the test service
            if i % 10 == 0:
                time.sleep(1)
        
        logger.info(f"🎯 Found {len(working_proxies)} working proxies out of {len(all_proxies)}")
        return working_proxies
    
    def should_refresh(self) -> bool:
        """Check if proxies should be refreshed"""
        if self.last_fetch_time is None:
            return True
        return (time.time() - self.last_fetch_time) > self.fetch_interval
    
    def get_cached_proxies(self) -> List[str]:
        """Get cached proxies without re-fetching"""
        return self.fetched_proxies.copy()
    
    def enable_source(self, source_name: str):
        """Enable a proxy source"""
        if source_name in self.sources:
            self.sources[source_name].enabled = True
            logger.info(f"Enabled source: {source_name}")
    
    def disable_source(self, source_name: str):
        """Disable a proxy source"""
        if source_name in self.sources:
            self.sources[source_name].enabled = False
            logger.info(f"Disabled source: {source_name}")
    
    def list_sources(self) -> Dict[str, bool]:
        """Get list of all sources and their enabled status"""
        return {name: source.enabled for name, source in self.sources.items()}


# Global proxy fetcher instance
proxy_fetcher = ProxyFetcher()


if __name__ == "__main__":
    """Test the proxy fetcher with AI quality checking"""
    print("🚀 MEGA Checker - AI Proxy Fetcher Test\n")
    
    fetcher = ProxyFetcher()
    
    # List available sources
    print("📋 Available proxy sources:")
    for name, enabled in fetcher.list_sources().items():
        status = "✅ Enabled" if enabled else "❌ Disabled"
        print(f"  - {name}: {status}")
    print()
    
    # Ask user for mode
    print("Choose mode:")
    print("  1. Fast Mode - Fetch only (no testing)")
    print("  2. AI Mode - Fetch + AI quality check (recommended)")
    print("  3. AI Elite Mode - Only highest quality proxies (score >= 80)")
    
    choice = input("\nEnter choice (1-3, default=1): ").strip() or "1"
    print()
    
    if choice == "1":
        # Fast mode - no testing
        print("🔄 Fast mode: Fetching proxies (no testing)...\n")
        proxies = fetcher.fetch_all_sources(max_proxies=100)
        
        if proxies:
            print(f"\n✅ Successfully fetched {len(proxies)} proxies")
            fetcher.save_to_file('fetched_proxies.txt')
            
            # Show first 10
            print("\n📝 First 10 proxies:")
            for i, proxy in enumerate(proxies[:10], 1):
                print(f"  {i}. {proxy}")
            
            print("\n💾 All proxies saved to: fetched_proxies.txt")
            print("\n⚠️ NOTE: These proxies are NOT tested and may be:")
            print("  - Slow or dead")
            print("  - Unreliable")
            print("  - Already flagged")
    
    elif choice == "2":
        # AI mode - quality testing
        print("🤖 AI mode: Fetching + quality testing...\n")
        high_quality_proxies = fetcher.fetch_high_quality(
            max_proxies=30,
            min_quality_score=60,
            test_sample_size=100,
            max_workers=15
        )
        
        if high_quality_proxies:
            print(f"\n✅ Successfully found {len(high_quality_proxies)} high-quality proxies")
            fetcher.save_to_file('ai_proxies_quality.txt', high_quality_proxies)
            
            print("\n📝 All high-quality proxies:")
            for i, proxy in enumerate(high_quality_proxies, 1):
                print(f"  {i:2}. {proxy}")
            
            print(f"\n💾 Saved to: ai_proxies_quality.txt")
            print("✨ These proxies are AI-tested and verified!")
    
    elif choice == "3":
        # Elite mode - only best
        print("🏆 Elite mode: Only highest quality proxies...\n")
        elite_proxies = fetcher.fetch_high_quality(
            max_proxies=20,
            min_quality_score=80,
            test_sample_size=150,
            max_workers=20
        )
        
        if elite_proxies:
            print(f"\n✅ Successfully found {len(elite_proxies)} elite proxies")
            fetcher.save_to_file('ai_proxies_elite.txt', elite_proxies)
            
            print("\n📝 Elite proxies:")
            for i, proxy in enumerate(elite_proxies, 1):
                print(f"  {i:2}. {proxy}")
            
            print(f"\n💾 Saved to: ai_proxies_elite.txt")
            print("🌟 These are the BEST proxies available!")
        else:
            print("\n⚠️ No proxies met elite quality standards")
            print("💡 Try AI Mode (option 2) with lower threshold")
    
    else:
        print("❌ Invalid choice")
    
    print("\n" + "="*70)
    print("ℹ️  TIP: Use AI Mode for best balance of speed and quality!")
    print("="*70)
