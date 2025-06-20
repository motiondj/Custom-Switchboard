# Custom Switchboard (테스트 버전)

**⚠️ 주의: 이는 테스트 버전입니다. 프로덕션 환경에서 사용하지 마세요.**

Epic Games의 Switchboard를 기반으로 한 **테스트용 커스터마이즈 버전**입니다. 기존 Switchboard의 주요 문제점들을 해결하고 개선된 기능을 제공합니다.

## 🎯 핵심 차이점 (기존 Switchboard 대비)

### 1. **관리자 권한 자동 요청** ⭐ 핵심 개선사항
```
기존 Switchboard: 수동으로 관리자 권한 설정 필요
Custom Switchboard: 실행 시 자동으로 관리자 권한 요청
```
- **문제**: 기존에는 GPU 클럭 제어 시 "Failed to obtain/convert traceback!" 오류 발생
- **해결**: Windows 매니페스트를 통한 자동 권한 요청으로 문제 완전 해결

### 2. **오류 처리 개선** ⭐ 핵심 개선사항
```
기존 Switchboard: "Failed to obtain/convert traceback!" 오류 발생
Custom Switchboard: 상세한 오류 메시지와 해결 방법 제공
```
- **문제**: 기존의 추적 불가능한 오류들
- **해결**: 구체적인 오류 정보와 디버깅 가이드 제공

### 3. **빌드 프로세스 개선**
```
기존 Switchboard: 관리자 권한 관련 빌드 문제
Custom Switchboard: 자동 권한 요청이 포함된 실행 파일 생성
```

## 🚨 테스트 버전 주의사항

### ⚠️ 중요 알림
- **이 버전은 테스트 목적으로만 사용하세요**
- **프로덕션 환경에서 사용하지 마세요**
- **기존 Switchboard를 대체하지 않습니다**
- **Epic Games 공식 지원 대상이 아닙니다**

### 🔬 테스트 목적
1. 관리자 권한 자동 요청 기능 검증
2. 오류 처리 개선 효과 확인
3. 사용자 경험 개선 테스트
4. 성능 최적화 검증

## 🛠️ 설치 및 테스트

### 1. 테스트 환경 설정
```bash
git clone <repository-url>
cd Switchboard
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 빌드 (관리자 권한 자동 요청 포함)
```bash
python -m PyInstaller Switchboard.spec
```

### 3. 테스트 실행
```bash
# dist/Switchboard.exe 실행
# 자동으로 관리자 권한 요청 창이 나타남
```

## 🔍 테스트 포인트

### 1. 관리자 권한 테스트
- [ ] 실행 시 자동 권한 요청 창 표시
- [ ] GPU 클럭 제어 기능 정상 작동
- [ ] "Failed to obtain/convert traceback!" 오류 해결 확인

### 2. 오류 처리 테스트
- [ ] 상세한 오류 메시지 표시
- [ ] 문제 해결 가이드 제공
- [ ] 디버깅 정보 개선 확인

### 3. 성능 테스트
- [ ] 메모리 사용량 최적화
- [ ] 응답성 향상 확인
- [ ] 안정성 개선 검증

## 📋 시스템 요구사항

### 필수 요구사항
- **운영체제**: Windows 10/11 (64-bit)
- **Python**: 3.11 이상
- **Unreal Engine**: 5.0 이상
- **관리자 권한**: 자동 요청됨

### 테스트 권장사항
- **GPU**: NVIDIA RTX 시리즈 (GPU 클럭 제어 테스트용)
- **네트워크**: 1Gbps 이상 (멀티 디바이스 테스트용)

## 🔧 주요 변경사항

### Switchboard.spec 수정
```python
# Windows 관리자 권한 요청을 위한 매니페스트 추가
manifest = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>'''
```

### .gitignore 추가
- 빌드 아티팩트 관리
- 캐시 파일 제외
- 로그 파일 관리

## 🎮 테스트 시나리오

### 시나리오 1: 기본 실행 테스트
1. Switchboard.exe 실행
2. 관리자 권한 요청 창 확인
3. 정상 실행 확인

### 시나리오 2: GPU 클럭 제어 테스트
1. nDisplay 설정에서 GPU 클럭 잠금 활성화
2. 오류 없이 정상 작동 확인
3. 성능 개선 효과 확인

### 시나리오 3: 오류 처리 테스트
1. 의도적으로 오류 상황 생성
2. 상세한 오류 메시지 확인
3. 해결 방법 가이드 확인

## 📊 테스트 결과 기록

### 성공한 테스트
- [ ] 관리자 권한 자동 요청
- [ ] GPU 클럭 제어 기능
- [ ] 오류 처리 개선

### 발견된 문제
- [ ] (테스트 중 발견된 문제들 기록)

### 개선 제안
- [ ] (추가 개선사항 제안)

## 🔄 버전 정보

- **버전**: 1.0.0 (테스트)
- **기반**: Epic Games Switchboard
- **상태**: 테스트 버전
- **목적**: 기능 개선 검증

## 📞 피드백 및 이슈

### 테스트 피드백
- 발견한 문제점이나 개선사항을 이슈로 등록
- 테스트 결과 공유
- 추가 기능 요청

### 알려진 제한사항
- Epic Games 공식 지원 아님
- 프로덕션 환경 미지원
- 일부 기능이 테스트 중

## 📝 변경 로그

### v1.0.0 (테스트)
- **관리자 권한 자동 요청**: Windows 매니페스트를 통한 자동 권한 요청
- **오류 처리 개선**: "Failed to obtain/convert traceback!" 오류 해결
- **빌드 프로세스 개선**: 자동 권한 요청이 포함된 실행 파일 생성
- **테스트 환경 구축**: 테스트용 설정 및 가이드 추가

---

**⚠️ 중요**: 이 Custom Switchboard는 **테스트 버전**입니다. Epic Games의 공식 Switchboard를 대체하지 않으며, 프로덕션 환경에서 사용하지 마세요. 테스트 목적으로만 사용하시기 바랍니다. 