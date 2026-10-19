import request from "@/utils/request"


/**
 * 创建预约
 * @param {*} data 
 * @returns 
 */
export function createReservation(data) {
    return request({
        url: '/api/reservation',
        method: 'post',
        data
    })
}