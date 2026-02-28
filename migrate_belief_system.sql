-- ============================================
-- Destiny City 数据库兼容性变更脚本
-- 新增：信仰体系（预测体系）功能
-- 适用于：SQLite
-- 执行方式：sqlite3 destiny.db < migrate_belief_system.sql
-- ============================================

-- 1. questions 表增加 belief_systems 字段
-- 标记每道题属于哪个信仰体系（逗号分隔：bazi,tarot,none 或 all）
ALTER TABLE questions ADD COLUMN belief_systems VARCHAR(100) NOT NULL DEFAULT 'all';

-- 2. user_results 表增加 belief_system 字段
-- 记录用户选择的信仰体系
ALTER TABLE user_results ADD COLUMN belief_system VARCHAR(20) NOT NULL DEFAULT 'all';

-- 3. test_progress 表增加 belief_system 字段
-- 保存答题中途的信仰体系选择
ALTER TABLE test_progress ADD COLUMN belief_system VARCHAR(20) NOT NULL DEFAULT 'all';

-- 4. 更新现有题目的 belief_systems 标签
-- 元素亲和（Q1, Q11）→ 通用
UPDATE questions SET belief_systems = 'bazi,tarot,none' WHERE category = '元素亲和';

-- 塔罗牌指引（Q2, Q7, Q13）→ 塔罗专属
UPDATE questions SET belief_systems = 'tarot' WHERE category = '塔罗牌指引';

-- 五行感应（Q3, Q9, Q16）→ 生辰八字专属
UPDATE questions SET belief_systems = 'bazi' WHERE category = '五行感应';

-- 星座能量（Q4, Q10, Q15）→ 塔罗/西方体系
UPDATE questions SET belief_systems = 'tarot' WHERE category = '星座能量';

-- 生活方式（Q5, Q12, Q17）→ 通用
UPDATE questions SET belief_systems = 'bazi,tarot,none' WHERE category = '生活方式';

-- 能量频率（Q6, Q8, Q14, Q18）→ 通用
UPDATE questions SET belief_systems = 'bazi,tarot,none' WHERE category = '能量频率';

-- 职业发展（Q8）→ 通用
UPDATE questions SET belief_systems = 'bazi,tarot,none' WHERE category = '职业发展';

-- 5. 新增"职业态度"类别题目（3道）
-- 注意：如果已经有 order_num 19-21 的题目则跳过
INSERT OR IGNORE INTO questions (order_num, category, belief_systems, content, options) VALUES
(19, '职业态度', 'bazi,tarot,none', '关于"卷"和"躺平"，你内心真实的声音是？', '[{"id":"19a","content":"我就是卷王本王，不拼命我会焦虑","weights":[0.8,0.0,0.2,0.2,0.7,0.0,0.5,0.1,0.0,0.9]},{"id":"19b","content":"躺平是一种智慧，人生何必那么累","weights":[0.0,0.5,0.1,0.5,0.0,0.7,0.0,0.3,0.6,0.0]},{"id":"19c","content":"我选择\u201c半躺\u201d\u2014\u2014该拼的时候拼，该享受的时候享受","weights":[0.3,0.3,0.4,0.4,0.3,0.4,0.3,0.4,0.3,0.3]},{"id":"19d","content":"我不想被别人定义的赛道绑架，我要走自己的路","weights":[0.4,0.1,0.8,0.1,0.2,0.3,0.8,0.2,0.3,0.4]}]'),
(20, '职业态度', 'bazi,tarot,none', '如果不考虑收入，你最想过哪种工作状态？', '[{"id":"20a","content":"带领一个团队攻克难关，改变一个行业","weights":[0.7,0.0,0.3,0.2,0.8,0.0,0.6,0.1,0.0,0.9]},{"id":"20b","content":"在一个安静的地方做手艺活，慢慢打磨作品","weights":[0.0,0.4,0.1,0.6,0.2,0.5,0.0,0.8,0.5,0.1]},{"id":"20c","content":"今天在巴厘岛写代码，明天在清迈画画\u2014\u2014数字游民","weights":[0.3,0.2,0.8,0.0,0.2,0.3,0.9,0.3,0.3,0.3]},{"id":"20d","content":"什么都不做也行，发呆、散步、看云，活着本身就够了","weights":[0.0,0.6,0.2,0.4,0.0,0.8,0.0,0.4,0.7,0.0]}]'),
(21, '职业态度', 'bazi,tarot,none', '面对一份\u201c钱多事少离家近\u201d和一份\u201c有挑战但可能改变世界\u201d的工作，你会？', '[{"id":"21a","content":"毫不犹豫选挑战\u2014\u2014人生就是要折腾","weights":[0.8,0.0,0.4,0.1,0.5,0.0,0.7,0.1,0.1,0.8]},{"id":"21b","content":"钱多事少离家近，这才是人间清醒","weights":[0.0,0.4,0.0,0.7,0.1,0.6,0.0,0.2,0.3,0.1]},{"id":"21c","content":"取决于那份挑战是否是我真正热爱的方向","weights":[0.3,0.3,0.3,0.3,0.3,0.3,0.4,0.5,0.5,0.4]},{"id":"21d","content":"两个都不选，我要自己创造第三条路","weights":[0.5,0.1,0.7,0.1,0.3,0.2,0.8,0.2,0.2,0.6]}]');

-- 6. 新增"城市硬指标"类别题目（4道，science 体系专属）
INSERT OR IGNORE INTO questions (order_num, category, belief_systems, content, options) VALUES
(22, '城市硬指标', 'science', '选城市时，你最看重的硬性条件是？', '[{"id":"22a","content":"就业机会多、薪资天花板高","weights":[0.7,0.0,0.3,0.2,0.8,0.0,0.5,0.0,0.0,0.9]},{"id":"22b","content":"医疗资源丰富、三甲医院多","weights":[0.0,0.5,0.0,0.7,0.3,0.5,0.0,0.2,0.4,0.1]},{"id":"22c","content":"教育资源好、名校集中","weights":[0.2,0.3,0.1,0.5,0.5,0.4,0.1,0.5,0.3,0.4]},{"id":"22d","content":"房价合理、生活成本可控","weights":[0.0,0.4,0.1,0.8,0.1,0.7,0.0,0.3,0.5,0.0]}]'),
(23, '城市硬指标', 'science', '你理想的通勤和居住状态是？', '[{"id":"23a","content":"住市中心，走路就能上班，享受便利","weights":[0.5,0.0,0.2,0.2,0.7,0.0,0.3,0.3,0.0,0.5]},{"id":"23b","content":"郊区大房子，有车有花园，不怕远","weights":[0.0,0.3,0.1,0.8,0.2,0.7,0.0,0.4,0.4,0.1]},{"id":"23c","content":"租房即可，随时能换城市的灵活感","weights":[0.3,0.1,0.8,0.0,0.1,0.2,0.9,0.1,0.2,0.3]},{"id":"23d","content":"小城市自有一套房，安稳过日子","weights":[0.0,0.5,0.0,0.7,0.0,0.8,0.0,0.3,0.6,0.0]}]'),
(24, '城市硬指标', 'science', '对一座城市的公共服务，你最在意什么？', '[{"id":"24a","content":"地铁发达、交通便利，去哪都方便","weights":[0.4,0.1,0.5,0.3,0.5,0.2,0.3,0.2,0.1,0.4]},{"id":"24b","content":"空气好、公园多、适合养生","weights":[0.0,0.5,0.3,0.5,0.0,0.8,0.0,0.4,0.6,0.0]},{"id":"24c","content":"文化活动丰富，博物馆、展览、演出多","weights":[0.2,0.3,0.3,0.2,0.3,0.3,0.2,0.8,0.4,0.2]},{"id":"24d","content":"办事效率高、政策透明、营商环境好","weights":[0.5,0.0,0.2,0.4,0.7,0.1,0.4,0.1,0.0,0.7]}]'),
(25, '城市硬指标', 'science', '如果让你用数据选城市，哪个排行榜最能打动你？', '[{"id":"25a","content":"人均GDP和薪资水平排行","weights":[0.6,0.0,0.2,0.2,0.8,0.0,0.4,0.0,0.0,0.8]},{"id":"25b","content":"宜居城市/幸福指数排行","weights":[0.0,0.5,0.2,0.6,0.1,0.7,0.0,0.4,0.5,0.0]},{"id":"25c","content":"创新/创业生态指数排行","weights":[0.5,0.0,0.6,0.1,0.5,0.1,0.7,0.2,0.1,0.7]},{"id":"25d","content":"文化/艺术/夜生活丰富度排行","weights":[0.2,0.3,0.4,0.2,0.2,0.3,0.3,0.8,0.3,0.2]}]');

-- ============================================
-- 验证变更
-- ============================================
-- SELECT id, order_num, category, belief_systems FROM questions ORDER BY order_num;
-- SELECT sql FROM sqlite_master WHERE name = 'user_results';
-- SELECT sql FROM sqlite_master WHERE name = 'test_progress';
