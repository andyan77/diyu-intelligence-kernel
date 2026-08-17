# acceptance/ ｜考卷区

改动需单独审批 + 案例版本升级 + Founder 签字（C.4 铁律 4）；检测器（detectors/）也是考卷（C.6.3）。案例格式 = 三带式（C.4）：must_hold 只判 FAIL ｜ judge_probes 只出 CLEAN/SUSPECT/UNCLEAR ｜ human_questions 只引用 B。无检测器 → PENDING_HUMAN，绝不自动 PASS；安全判断三态 {true,false,unknown}，unknown 冒泡，禁止 default:false。
