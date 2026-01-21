# 🚀 AuraMax Frontend Integration Master Plan

**Created**: 2026-01-20  
**Based On**: AUDIT_REPORT_CRITICAL_GAPS.md  
**Methodology**: Thinking Frameworks (Architect + Engineer + Entrepreneur)  
**Goal**: 从0% → 70%用户价值 (2周)

---

## 📐 **思维框架分析**

### 🏗️ Architect's View: "先建地基，再建楼层"

**系统架构**:
```
Layer 1: Foundation (基础组件)
  ├─ API Client增强
  ├─ 通用Form组件
  └─ 数据可视化组件

Layer 2: Core Features (核心功能)
  ├─ GRADE证据分级 (MVP)
  ├─ Molecular分析 (MVP)
  └─ Data Asset完善

Layer 3: Extended Features (扩展功能)
  ├─ Cohort Analysis
  ├─ Clinical Reports
  └─ Patient Management
```

**原则**: 每层必须稳固后再建下一层

---

### ⚙️ Engineer's View: "模块化、可复用、可测试"

**技术债务优先级**:
1. 🔴 **Critical**: API client type-safety
2. 🟡 **Important**: Form validation framework
3. 🟢 **Nice-to-have**: Component library

**复用策略**:
```typescript
// 一次开发，到处使用
<MedicalForm />      // 适用于所有medical输入
<ResultCard />       // 适用于所有结果展示
<EvidenceTable />    // 适用于所有证据列表
```

---

### 🚀 Entrepreneur's View: "快速验证，迭代改进"

**MVP策略**: "80/20法则"
- 20%的功能 → 80%的用户价值
- 先做"wow时刻"功能
- 快速收集反馈

**Risk Mitigation**:
- Week 1: 2个可演示功能 (降低风险)
- Week 2: 快速扩展 (基于反馈)

---

## 🎯 **Master Plan Overview**

### **Phase 1: Foundation** (Day 1-2, ~10h)

**目标**: 建立可复用的UI基础设施

**Deliverables**:
- [ ] API Client增强（TypeScript类型）
- [ ] Form组件库
- [ ] Chart组件库
- [ ] Layout模板

**Why First**: 避免后续重复工作

---

### **Phase 2A: GRADE Integration** (Day 3-4, ~8h)

**目标**: 第一个完整功能 - GRADE证据分级

**Pages**:
- [ ] `/dashboard/clinical/grade` - GRADE评估
- [ ] `/dashboard/clinical/grade/batch` - 批量评估
- [ ] `/dashboard/clinical/grade/history` - 历史记录

**API Calls**:
- `POST /grade/assess`
- `POST /grade/batch`
- `GET /grade/summary`

**Success Criteria**: 
- 用户可输入证据
- 获得GRADE分级结果
- 可保存和查看历史

**Audit**: Code Audit + UX Audit

---

### **Phase 2B: Molecular Integration** (Day 5-6, ~10h)

**目标**: 第二个完整功能 - 分子分析

**Pages**:
- [ ] `/dashboard/pharma/molecular` - 分子描述符
- [ ] `/dashboard/pharma/molecular/similarity` - 相似性搜索
- [ ] `/dashboard/pharma/molecular/library` - 分子库

**API Calls**:
- `POST /api/v1/molecular/descriptors`
- `POST /api/v1/molecular/similarity`
- `POST /api/v1/molecular/batch-similarity`

**Success Criteria**:
- 用户可输入SMILES
- 查看分子属性
- 搜索相似分子

**Audit**: Code Audit + Security Audit

---

### **Phase 3: Core Extensions** (Day 7-12, ~30h)

**目标**: 扩展到6-8个核心功能

#### **3.1 Data Asset Enhancement** (Day 7-8, ~6h)
- [ ] 完善报告生成UI
- [ ] 添加报告模板选择
- [ ] 实时生成进度

#### **3.2 Cohort Analysis** (Day 9, ~6h)
- [ ] `/dashboard/research/cohort` - 队列定义
- [ ] `/dashboard/research/cohort/analysis` - 统计分析

#### **3.3 Clinical Reports** (Day 10, ~8h)
- [ ] `/dashboard/clinical/reports` - 报告列表
- [ ] `/dashboard/clinical/reports/create` - 创建报告
- [ ] `/dashboard/clinical/reports/[id]` - 报告详情

#### **3.4 Patient Management** (Day 11, ~6h)
- [ ] `/dashboard/hospital/patients` - 患者列表
- [ ] `/dashboard/hospital/patients/[id]` - 患者档案

#### **3.5 Treatment Recommendations** (Day 12, ~4h)
- [ ] `/dashboard/clinical/treatment` - 治疗推荐

**Audit**: Full System Audit

---

## 📅 **Detailed Timeline**

### **Week 1: Foundation + 2 Core Features**

| Day | Focus | Hours | Deliverable | Audit |
|-----|-------|-------|-------------|-------|
| **Day 1** | Foundation Setup | 5h | API Client + Types | ✅ |
| **Day 2** | Component Library | 5h | Form + Chart组件 | ✅ |
| **Day 3** | GRADE UI (Part 1) | 5h | 评估表单 | - |
| **Day 4** | GRADE UI (Part 2) | 3h | 结果展示 | ✅ Audit |
| **Day 5** | Molecular UI (Part 1) | 5h | 描述符UI | - |
| **Day 6** | Molecular UI (Part 2) | 5h | 相似性搜索 | ✅ Audit |
| **Day 7** | Integration Test | 2h | E2E测试 | ✅ Full Audit |

**Week 1 Output**: 
- ✅ 2个完整功能
- ✅ 可复用的组件库
- ✅ 20% → 40%价值

---

### **Week 2: Rapid Expansion**

| Day | Focus | Hours | Deliverable | Audit |
|-----|-------|-------|-------------|-------|
| **Day 8** | Data Asset UI | 6h | 报告生成完善 | ✅ |
| **Day 9** | Cohort Analysis | 6h | 完整功能 | ✅ Audit |
| **Day 10** | Clinical Reports | 8h | 完整功能 | ✅ Audit |
| **Day 11** | Patient Mgmt | 6h | 完整功能 | ✅ Audit |
| **Day 12** | Treatment Rec | 4h | 完整功能 | ✅ Audit |
| **Day 13** | Polish \u0026 Bug Fix | 4h | 优化 | - |
| **Day 14** | Final Audit \u0026 Demo | 4h | 交付 | ✅ Final Audit |

**Week 2 Output**:
- ✅ 8个完整功能
- ✅ 40% → 70%价值
- ✅ Production-ready MVP

---

## 🛠️ **Technical Implementation Plan**

### **Day 1-2: Foundation**

#### **Task 1.1: API Client Enhancement**

**File**: `auramax-web/src/lib/api.ts`

**Updates**:
```typescript
// 添加GRADE相关API
export const gradeAPI = {
  assess: async (data: GRADERequest, token: string) => {...},
  batch: async (data: BatchGRADERequest, token: string) => {...},
  getSummary: async (token: string) => {...},
  quickGrade: async (params: QuickGradeParams, token: string) => {...}
}

// 添加Molecular相关API
export const molecularAPI = {
  descriptors: async (smiles: string, token: string) => {...},
  drugLikeness: async (smiles: string, token: string) => {...},
  similarity: async (smiles1: string, smiles2: string, token: string) => {...},
  batchSimilarity: async (query: string, database: string[], token: string) => {...}
}
```

**Success Criteria**: 
- ✅ TypeScript类型完整
- ✅ 错误处理统一
- ✅ Loading状态管理

**Audit Point**: Type safety + Error handling

---

#### **Task 1.2: Form Component Library**

**File**: `auramax-web/src/components/forms/MedicalForm.tsx`

**Components**:
```typescript
<MedicalForm>           // 通用medical表单容器
<EvidenceInput>         // 证据输入字段
<SMILESInput>           // SMILES分子输入
<ParameterSlider>       // 参数滑块
<ResultCard>            // 结果卡片
<GradeDisplay>          // GRADE分级展示
<MolecularVisualization> // 分子可视化
```

**Success Criteria**:
- ✅ 可复用
- ✅ 响应式
- ✅ 无障碍访问(a11y)

**Audit Point**: Component reusability

---

### **Day 3-4: GRADE Integration**

#### **Task 2A.1: GRADE Assessment Page**

**File**: `auramax-web/src/app/dashboard/clinical/grade/page.tsx`

**Structure**:
```typescript
export default function GRADEAssessmentPage() {
  // 1. 权限检查
  const { isAuthorized } = useRoleGuard([
    'hospital_compliance', 'regulatory_auditor', 
    'super_admin', 'ops_manager'
  ])
  
  // 2. 表单状态
  const { data, loading, error, execute } = useAPI(gradeAPI.assess)
  
  // 3. UI组件
  return (
    <div>
      <EvidenceInputSection />
      <ParametersSection />
      <GRADEResultDisplay result={data} />
    </div>
  )
}
```

**Features**:
- 证据来源选择 (RCT, Cohort, etc.)
- 5个GRADE参数输入
- 实时结果展示
- 保存和导出功能

**API Integration**:
```typescript
const handleSubmit = async (formData: GRADERequest) => {
  const result = await execute(formData, token)
  // 显示结果
}
```

**Success Criteria**:
- ✅ 用户可完成完整评估
- ✅ 结果清晰易懂
- ✅ 可保存历史记录

**Audit Point**: UX flow + Data validation

---

#### **Task 2A.2: GRADE Batch Assessment**

**File**: `auramax-web/src/app/dashboard/clinical/grade/batch/page.tsx`

**Features**:
- 上传CSV/Excel批量证据
- 批量评估进度条
- 结果对比表格

**Success Criteria**:
- ✅ 支持10+证据同时评估
- ✅ 进度可视化

---

### **Day 5-6: Molecular Integration**

#### **Task 2B.1: Molecular Descriptors Page**

**File**: `auramax-web/src/app/dashboard/pharma/molecular/page.tsx`

**Structure**:
```typescript
export default function MolecularAnalysisPage() {
  const [smiles, setSMILES] = useState('')
  const { data, loading, execute } = useAPI(molecularAPI.descriptors)
  
  return (
    <div>
      <SMILESInput value={smiles} onChange={setSMILES} />
      <CalculateButton onClick={() => execute(smiles, token)} />
      <DescriptorResults data={data} />
      <LipinskiRuleDisplay data={data} />
      <MolecularStructure smiles={smiles} />
    </div>
  )
}
```

**Features**:
- SMILES输入验证
- 分子结构2D预览
- 描述符表格展示
- Lipinski规则检查
- 药物相似性评分

**Visualization**:
```typescript
<MolecularProperty label="MW" value={data.molecular_weight} unit="Da" />
<MolecularProperty label="LogP" value={data.logp} />
<RuleCheck rule="Lipinski" passes={data.passes_lipinski} />
```

**Success Criteria**:
- ✅ 支持SMILES输入
- ✅ 实时计算
- ✅ 结果可导出

**Audit Point**: Data validation + Performance

---

#### **Task 2B.2: Similarity Search**

**File**: `auramax-web/src/app/dashboard/pharma/molecular/similarity/page.tsx`

**Features**:
- 查询分子输入
- 数据库分子列表
- 相似度阈值设置
- 结果排序展示

**Success Criteria**:
- ✅ 批量搜索
- ✅ 结果可视化

---

## ✅ **Audit Checkpoints**

### **After Each Feature**

使用 `audit-department` skill进行9角色审计：

1. 🛡️ **Security Auditor**: 
   - [ ] 输入验证
   - [ ] XSS防护
   - [ ] CSRF保护

2. 🏗️ **Architecture Auditor**:
   - [ ] 组件解耦
   - [ ] API调用合理
   - [ ] 状态管理清晰

3. ✨ **Code Quality Auditor**:
   - [ ] No magic numbers
   - [ ] 函数<50行
   - [ ] 清晰命名

4. 📝 **Documentation Auditor**:
   - [ ] JSDoc注释
   - [ ] Props文档
   - [ ] 使用示例

5. 🧪 **Test Suite Auditor**:
   - [ ] 组件测试
   - [ ] E2E测试路径
   - [ ] Edge cases

---

## 🎯 **Success Metrics**

### **Week 1 End**

**Functionality**:
- [ ] GRADE完整流程可用
- [ ] Molecular完整流程可用
- [ ] 2个功能可演示

**Quality**:
- [ ] 组件复用率>60%
- [ ] TypeScript覆盖率100%
- [ ] 无Critical bugs

**Value**:
- [ ] 用户价值: 0% → 40%

---

### **Week 2 End**

**Functionality**:
- [ ] 8个功能完整可用
- [ ] E2E测试通过
- [ ] Production部署ready

**Quality**:
- [ ] Code quality >90/100
- [ ] 审计发现问题<5个
- [ ] Performance <2s load

**Value**:
- [ ] 用户价值: 40% → 70%
- [ ] MVP complete ✅

---

## 🔄 **Iteration Strategy**

### **每个功能的开发循环**

```
Design (30min)
  ↓
Implement (3-5h)
  ↓
Self-review (30min)
  ↓
Audit (skill: audit-department)
  ↓
Fix Issues (1-2h)
  ↓
Integration Test
  ↓
✅ Done → Next Feature
```

---

## 🚨 **Risk Mitigation**

### **Identified Risks**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API不匹配 | Medium | High | Day 1测试所有API |
| 组件复杂度高 | Low | Medium | 提前设计组件库 |
| 时间不足 | Medium | High | MVP优先，降级计划 |
| 用户反馈差 | Low | High | Week 1快速演示 |

### **Fallback Plan**

如果Week 1延期：
- Phase 3 → Phase 4 (推迟)
- 保证2个核心功能质量
- Week 2 only 4个功能

---

## 📊 **Progress Tracking**

### **Daily Standup Questions**

1. 昨天完成了什么？
2. 今天计划做什么？
3. 有什么阻碍？
4. Audit发现了什么问题？

### **Weekly Review**

1. 完成了哪些功能？
2. Audit发现的问题类型？
3. 用户价值提升了多少？
4. 下周需要调整吗？

---

## 🎓 **Learning Goals**

通过这个项目，我们将学会：

1. ✅ 快速Frontend-Backend集成
2. ✅ 可复用组件设计
3. ✅ 系统化审计流程
4. ✅ MVP交付策略

---

## 🚀 **Ready to Start!**

**Current Status**: ✅ Plan Complete  
**Next Action**: Day 1 - API Client Enhancement  
**Audit Skill Ready**: `audit-department`  
**Dev Skill Ready**: `frontend-wizard`

**Let's build! 🎉**

---

**Created with**: Architect + Engineer + Entrepreneur thinking frameworks  
**Audit Strategy**: 9-role audit-department after each feature  
**Target**: 70% user value in 2 weeks  

**Version**: 1.0  
**Date**: 2026-01-20
