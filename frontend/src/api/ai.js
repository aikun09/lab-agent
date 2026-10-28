import request from '@/utils/request'

/**
 * ai对话请求
 */
export function chatApi(data) {
  return request({
    url: '/api/ai/chat',
    method: 'post',
    data,
    timeout: 90000
  })
}