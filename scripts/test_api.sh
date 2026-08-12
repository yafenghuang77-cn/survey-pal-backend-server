#!/bin/bash
# 测试接口脚本 - 验证所有测试接口响应格式

set -e

BASE_URL="${1:-http://localhost:8000}"

echo "🧪 测试调研宝后端 API 接口"
echo "Base URL: $BASE_URL"
echo ""

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

test_endpoint() {
    local method=$1
    local path=$2
    local data=$3
    local desc=$4

    echo -n "Testing $desc ... "

    if [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$BASE_URL$path")
    else
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$path")
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓${NC} ($http_code)"
        echo "$body" | jq -C '.' 2>/dev/null || echo "$body"
    else
        echo -e "${RED}✗${NC} ($http_code)"
        echo "$body"
    fi
    echo ""
}

# 测试所有接口
test_endpoint "GET" "/health/live" "" "健康检查 - 存活"
test_endpoint "GET" "/health/ready" "" "健康检查 - 就绪"
test_endpoint "GET" "/api/v1/test" "" "基础测试接口"
test_endpoint "GET" "/api/v1/version" "" "版本信息"
test_endpoint "POST" "/api/v1/echo" '{"message":"Hello World"}' "回显接口"
test_endpoint "GET" "/api/v1/list?page=1&page_size=5" "" "分页列表(第1页)"
test_endpoint "GET" "/api/v1/list?page=2&page_size=10" "" "分页列表(第2页)"
test_endpoint "GET" "/api/v1/error-demo?code=10001" "" "错误响应 - 参数校验失败"
test_endpoint "GET" "/api/v1/error-demo?code=11002" "" "错误响应 - Token过期"
test_endpoint "GET" "/api/v1/exception-demo" "" "异常处理器测试"

echo ""
echo "✅ 测试完成"
