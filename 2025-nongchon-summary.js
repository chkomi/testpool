document.addEventListener('DOMContentLoaded', () => {
    const target = document.getElementById('summary-content');
    const fileInput = document.getElementById('file-input');
    const btnLoadLocal = document.getElementById('btn-load-local');
    const searchBox = document.getElementById('search-box');
    const progressBar = document.getElementById('progress-bar');
    const isStatic = target?.dataset?.static === 'true';
    
    let allSections = [];
    let originalContent = '';
    
    // Helper functions for enhanced rendering
    // Remove this function since we're not using tables anymore
    const shouldConvertToTable = () => false;
    
    const createBadge = (type, text) => {
        const badgeClass = type === 'included' ? 'badge-success' : 
                          type === 'excluded' ? 'badge-error' : 
                          type === 'important' ? 'badge-warning' : 'badge-info';
        const icon = type === 'included' ? '✅' : 
                    type === 'excluded' ? '❌' : 
                    type === 'important' ? '⚠️' : 'ℹ️';
        return `<span class="badge ${badgeClass}">${icon} ${text}</span>`;
    };
    
    const extractArticleReference = (text) => {
        const match = text.match(/\(제\d+조[^)]*?\)/);
        return match ? match[0] : null;
    };
    
    const isLawSection = (line) => {
        return line.includes('조)') || line.includes('령 제') || line.includes('법 제');
    };

    const parseAndRender = (text) => {
        if (!text) {
            target.innerHTML = '<p>내용이 없습니다.</p>';
            return;
        }

        originalContent = text;
        const lines = text.trim().split('\n');
        let html = '';
        let inTable = false;
        let inList = false;
        let inCodeBlock = false;
        let isInLawCard = false;
        allSections = [];

        lines.forEach((line, index) => {
            line = line.trim();
            
            // Remove unwanted markers
            if (line.startsWith('---') || line === '---' || (line.startsWith('####') && line.includes('---'))) {
                return; // Skip these lines completely
            }
            
            
            // Remove # symbols at the beginning and clean up
            if (line.startsWith('# ')) {
                const title = line.substring(2).trim();
                const id = 'section-' + allSections.length;
                allSections.push({ title, level: 1, id });
                html += `<h1 id="${id}">${title}</h1>`;
            } else if (line.startsWith('## ')) {
                const title = line.substring(3).trim();
                const id = 'section-' + allSections.length;
                allSections.push({ title, level: 2, id });
                html += `<h2 id="${id}">${title}</h2>`;
            } else if (line.startsWith('### ')) {
                const title = line.substring(4).trim();
                const id = 'section-' + allSections.length;
                const sectionNumber = allSections.filter(s => s.level === 3).length + 1;
                allSections.push({ title, level: 3, id });
                html += `<h3 id="${id}" data-number="${sectionNumber}">${title}</h3>`;
            } else if (line.startsWith('#### ')) {
                const title = line.substring(5).trim();
                const id = 'section-' + allSections.length;
                allSections.push({ title, level: 4, id });
                
                // Create clean section header
                const articleRef = extractArticleReference(title);
                const cleanTitle = title.replace(/\([^)]*\)/g, '').trim();
                
                html += `
                    <div class="section-header">
                        <h4 id="${id}">${cleanTitle}</h4>
                        ${articleRef ? `<span class="article-badge">${articleRef}</span>` : ''}
                    </div>
                `;
            } else if (line.startsWith('##### ')) {
                const title = line.substring(6).trim();
                const id = 'section-' + allSections.length;
                allSections.push({ title, level: 5, id });
                html += `<h5 id="${id}">${title}</h5>`;
            } else if (line.startsWith('```')) {
                if (inCodeBlock) {
                    html += '</code></pre>';
                    inCodeBlock = false;
                } else {
                    html += '<pre><code>';
                    inCodeBlock = true;
                }
            } else if (inCodeBlock) {
                html += line + '\n';
            } else if (line.startsWith('|')) {
                if (!inTable) {
                    html += '<table class="clean-table">';
                    inTable = true;
                }
                const cells = line.split('|').slice(1, -1);
                // Skip separator lines with dashes
                if (line.includes('---') && cells.every(cell => cell.trim().match(/^-+$/))) {
                    return; // Skip this line completely
                }
                
                // Check if this is the first row (header) by looking at content
                const isFirstRow = !html.includes('<tbody>');
                if (isFirstRow && cells.some(cell => cell.trim().includes('기간') || cell.trim().includes('내용') || cell.trim().includes('금액') || cell.trim().includes('비율'))) {
                    html += '<thead><tr>' + cells.map(cell => `<th>${cell.trim()}</th>`).join('') + '</tr></thead><tbody>';
                } else {
                    html += '<tr>' + cells.map(cell => `<td>${cell.trim().replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</td>`).join('') + '</tr>';
                }
            } else if (line.match(/^\d+\./) || line.startsWith('✅') || line.startsWith('❌')) {
                // Convert to simple text without numbers
                if (line.startsWith('✅') || line.startsWith('❌')) {
                    const cleanLine = line.replace(/^[✅❌]\s*/, '').replace(/^\d+\.\s*/, '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    
                    if (line.startsWith('✅')) {
                        html += `<div class="simple-item included">${cleanLine}</div>`;
                    } else if (line.startsWith('❌')) {
                        html += `<div class="simple-item excluded">${cleanLine}</div>`;
                    }
                } else if (line.match(/^\d+\./)) {
                    // Remove numbers from regular numbered lists too
                    const cleanLine = line.replace(/^\d+\.\s*/, '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    if (!inList) {
                        html += '<ul>';
                        inList = true;
                    }
                    html += `<li>${cleanLine}</li>`;
                } else {
                    if (inTable) {
                        html += '</div>';
                        inTable = false;
                    }
                    if (!inList) {
                        html += '<ul>';
                        inList = true;
                    }
                    html += `<li>${line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>`;
                }
            } else if (line.startsWith('<div class="highlight-box">') || line.startsWith('<div class="key-point">')) {
                if (inTable) {
                    html += inTable && html.includes('simple-list') ? '</div>' : '</tbody></table>';
                    inTable = false;
                }
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                html += line;
            } else {
                if (inTable) {
                    html += inTable && html.includes('simple-list') ? '</div>' : '</tbody></table>';
                    inTable = false;
                }
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                if (line && !line.startsWith('</div>')) {
                    // Check for special content patterns
                    if (line.includes('**') && (line.includes('포함') || line.includes('제외') || line.includes('중요'))) {
                        // Convert to info box for important notes
                        const content = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                        html += `<div class="info-box"><h5>중요사항</h5><p>${content}</p></div>`;
                    } else {
                        html += `<p>${line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</p>`;
                    }
                } else if (line) {
                    html += line;
                }
            }
        });

        if (inTable) html += inTable && html.includes('simple-list') ? '</div>' : '</tbody></table>';
        if (inList) html += '</ul>';
        if (inCodeBlock) html += '</code></pre>';

        target.innerHTML = html;
        buildToc();
    };

    const buildToc = () => {
        const toc = document.getElementById('toc-list');
        if (!toc) return;
        toc.innerHTML = '';

        // Use level 2 and 3 sections for TOC
        const items = allSections.filter(s => s.level === 2 || s.level === 3);
        items.forEach(({ id, title, level }) => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `#${id}`;
            a.textContent = title.replace(/^([#\d.\s✅❌📌🔥🎯📚📅💰📊]+)/, '').trim();
            a.style.paddingLeft = level === 3 ? '18px' : '8px';
            a.addEventListener('click', (e) => {
                e.preventDefault();
                const el = document.getElementById(id);
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                history.replaceState(null, '', `#${id}`);
            });
            li.appendChild(a);
            toc.appendChild(li);
        });

        // Populate quick cards with first 4 level-2 sections
        const qcWrap = document.querySelector('.quick-cards');
        if (qcWrap) {
            qcWrap.innerHTML = '';
            const topSections = allSections.filter(s => s.level === 2).slice(0, 5);
            topSections.forEach(({ id, title }) => {
                const a = document.createElement('a');
                a.className = 'quick-card';
                a.href = `#${id}`;
                a.textContent = title.replace(/^([#\d.\s✅❌📌🔥🎯📚📅💰📊]+)/, '').trim();
                a.addEventListener('click', (e) => {
                    e.preventDefault();
                    const el = document.getElementById(id);
                    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                });
                qcWrap.appendChild(a);
            });
        }

        // Scroll spy to highlight active link
        const anchors = Array.from(toc.querySelectorAll('a'));
        const sections = anchors.map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
        const onScroll = () => {
            let activeIndex = 0;
            const fromTop = window.scrollY + 100;
            for (let i = 0; i < sections.length; i++) {
                const sec = sections[i];
                if (sec.offsetTop <= fromTop) activeIndex = i; else break;
            }
            anchors.forEach((a, i) => a.classList.toggle('active', i === activeIndex));
        };
        window.removeEventListener('scroll', window.__tocScrollSpy || (() => {}));
        window.__tocScrollSpy = onScroll;
        window.addEventListener('scroll', onScroll);
        onScroll();
    };
    
    const renderText = (text) => {
        parseAndRender(text);
    };

    // Search functionality
    const highlightText = (text, term) => {
        if (!term) return text;
        const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<mark style="background: #fef3c7; padding: 2px 4px; border-radius: 3px;">$1</mark>');
    };

    const performSearch = (searchTerm) => {
        if (!searchTerm.trim()) {
            parseAndRender(originalContent);
            return;
        }
        
        const lines = originalContent.trim().split('\n');
        const matchingLines = [];
        const contextLines = 2;
        const searchRegex = new RegExp(searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
        
        lines.forEach((line, index) => {
            if (searchRegex.test(line)) {
                const start = Math.max(0, index - contextLines);
                const end = Math.min(lines.length - 1, index + contextLines);
                
                for (let i = start; i <= end; i++) {
                    if (!matchingLines.includes(i)) {
                        matchingLines.push(i);
                    }
                }
            }
        });
        
        if (matchingLines.length === 0) {
            target.innerHTML = `<div class="key-point">
                <p>🔍 "${searchTerm}" 검색 결과가 없습니다.</p>
                <p>다른 키워드로 검색해보세요.</p>
            </div>`;
            return;
        }
        
        const filteredContent = matchingLines.sort((a, b) => a - b)
            .map(lineIndex => highlightText(lines[lineIndex], searchTerm))
            .join('\n');
        
        parseAndRender(filteredContent);
        
        // Add search results header
        const resultHeader = document.createElement('div');
        resultHeader.className = 'key-point';
        resultHeader.innerHTML = `
            <p>🔍 "${searchTerm}" 검색 결과: ${matchingLines.length}개 라인</p>
            <button onclick="clearSearch()" style="background: var(--secondary-color); color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; margin-top: 0.5rem;">전체 내용 보기</button>
        `;
        target.insertBefore(resultHeader, target.firstChild);
    };

    // Global function for clearing search
    window.clearSearch = () => {
        searchBox.value = '';
        parseAndRender(originalContent);
    };

    // Search box event listener
    let searchTimeout;
    searchBox?.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, 300);
    });

    // Scroll progress indicator
    const updateScrollProgress = () => {
        if (!progressBar) return;
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = Math.min(100, Math.max(0, scrollPercent)) + '%';
    };

    window.addEventListener('scroll', updateScrollProgress);
    window.addEventListener('resize', updateScrollProgress);

    if (isStatic) {
        const staticContent = target.textContent;
        target.innerHTML = ''; // Clear original text content
        parseAndRender(staticContent);
    } else {
        if (location.protocol === 'file:') {
            target.innerHTML = '<p>로컬 파일 모드입니다. 아래 "로컬 파일 불러오기" 버튼을 눌러 농어촌정비법_완전정리.txt를 선택하세요.</p>';
        } else {
            const raw = '농어촌정비법_완전정리.txt';
            const candidates = [raw, './' + raw, encodeURI(raw), '/' + encodeURI(raw)];
            const tryFetchSequential = async (urls) => {
                let lastErr = null;
                for (const url of urls) {
                    try {
                        const res = await fetch(url, { cache: 'no-store' });
                        if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
                        const text = await res.text();
                        return text;
                    } catch (e) {
                        lastErr = e;
                        console.warn('요약 로드 실패 시도:', url, e);
                    }
                }
                throw lastErr || new Error('요약 파일 로드 실패');
            };

            tryFetchSequential(candidates)
                .then(renderText)
                .catch((err) => {
                    console.error(err);
                    target.innerHTML = '<p>요약 자동 로드에 실패했습니다. 서버가 루트에서 구동 중인지 확인하거나, "로컬 파일 불러오기"를 이용하세요.</p>';
                });
        }
    }

    // Enhanced toolbar actions
    document.getElementById('btn-copy')?.addEventListener('click', async () => {
        try {
            const textContent = target.innerText || '';
            await navigator.clipboard.writeText(textContent);
            
            // Show success feedback
            const btn = document.getElementById('btn-copy');
            const originalText = btn.textContent;
            btn.textContent = '✅ 복사됨!';
            btn.style.background = 'var(--success-color)';
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = 'var(--primary-color)';
            }, 2000);
        } catch {
            alert('복사에 실패했습니다. 브라우저 권한을 확인해주세요.');
        }
    });

    document.getElementById('btn-top')?.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    btnLoadLocal?.addEventListener('click', () => fileInput?.click());
    fileInput?.addEventListener('change', () => {
        const file = fileInput.files && fileInput.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) => renderText(String(e.target?.result || ''));
        reader.onerror = () => alert('파일을 읽는 중 오류가 발생했습니다.');
        reader.readAsText(file, 'utf-8');
    });

    // Add enhanced toolbar buttons
    const toolbar = document.querySelector('.summary-toolbar');
    if (toolbar) {
        // Add search toggle button
        const searchToggle = document.createElement('button');
        searchToggle.className = 'toolbar-btn';
        searchToggle.innerHTML = '🔍 검색 토글';
        searchToggle.addEventListener('click', () => {
            const searchContainer = document.querySelector('.search-container');
            if (searchContainer.style.display === 'none') {
                searchContainer.style.display = 'block';
                searchBox.focus();
            } else {
                searchContainer.style.display = 'none';
                clearSearch();
            }
        });
        
        // Add print button
        const printBtn = document.createElement('button');
        printBtn.className = 'toolbar-btn';
        printBtn.innerHTML = '🖨️ 인쇄';
        printBtn.addEventListener('click', () => {
            window.print();
        });
        
        toolbar.appendChild(searchToggle);
        toolbar.appendChild(printBtn);
    }
});
