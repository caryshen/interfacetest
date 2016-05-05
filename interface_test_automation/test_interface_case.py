#!/usr/bin/python3
# -*- coding:utf-8 -*-

import unittest


def update_result(self,id,param,result,reason):
    try:
        self.db1_cursor.execute('UPDATE test_result SET request_param = %s WHERE case_id = %s' ,(str(param), id))
        self.db1_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(result, id))
        self.db1_cursor.execute('UPDATE test_result SET reason = %s WHERE case_id = %s' ,(reason, id))
        self.db1_cursor.execute('commit')
    except Exception as e:
        print('%s' % e)
        self.db1_cursor.execute('rollback')

# 测试用例(组)类
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', test_data=None, http=None, db1_cursor=None, db2_cursor=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.test_data = test_data
        self.http = http
        self.db1_cursor = db1_cursor
        self.db2_cursor = db2_cursor


class TestInterfaceCase(ParametrizedTestCase):
    def setUp(self):
        pass
    #接口1.1测试
    def test_getcode(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '0','返回code不等于0'
            assert response['returnStatus']['errorCode'] == "",'errorCode不为空'
            assert response['returnStatus']['error'] == "",'失败原因不为空'
            assert response['data'] == {},'data不为空'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_getcode_missarg(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_getcode_errorarg(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute("UPDATE test_result SET result = %s WHERE case_id = %s" ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "phone_invalid_error",'errorCode不为phone_invalid_error'
            assert response['returnStatus']['error'] == "手机号码无效。",'失败原因不为手机号码无效'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    #接口1.2测试
    def test_login(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        #保存TOKEN
        # global TESTTOKEN
        # TESTTOKEN=str(response['data']['access_token'])
        try:
            assert response['returnStatus']['status'] == '0','返回code不等于0'
            assert response['returnStatus']['errorCode'] == "",'errorCode不为空'
            assert response['returnStatus']['error'] == "",'失败原因不为空'
            assert response['data']['userId'] != "",'userid不正确'
            assert response['data']['userNo'] != "",'userNo不正确'
            assert response['data']['nick'] != "",'nick不正确'
            assert response['data']['userType'] != "",'userType不正确'
            assert response['data']['portraitUrl'] != "",'portraitUrl不正确'
            assert response['data']['phone'] == "13901234567",'phone不正确'
            assert response['data']['name'] != "",'name不正确'
            assert response['data']['access_token'] != "",'access_token不正确'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_login_missarg(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
                return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)


    def test_login_phoneerror(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s',(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
                return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "phone_invalid_error",'errorCode不为phone_invalid_error'
            assert response['returnStatus']['error'] == "手机号码无效。",'失败原因不为手机号码无效。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_login_codeerror(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
                return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "logon_code_error",'errorCode不为logon_code_error'
            assert response['returnStatus']['error'] == "验证码有误，请重新输入。",'验证码有误，请重新输入。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
    #接口1.3测试
    def test_thirdlogin(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s',(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        #保存userNo
        global TESTUSERNO
        TESTUSERNO = response['data']['userNo']
        try:
           assert response['returnStatus']['status'] == '0','返回code不等于0'
           assert response['returnStatus']['errorCode'] == "",'errorCode不为空'
           assert response['returnStatus']['error'] == "",'失败原因不为空'
           assert response['data']['userId'] != "",'userid不正确'
           assert response['data']['userNo'] != "",'userNo不正确'
           assert response['data']['nick'] != "",'nick不正确'
           assert response['data']['userType'] != "",'userType不正确'
           assert response['data']['portraitUrl'] != "",'portraitUrl不正确'
           assert response['data']['name'] != "",'name不正确'
           assert response['data']['phone'] == "13482392797",'phone不正确'
           assert response['data']['newUser'] == "false",'newUser不正确'
           assert response['data']['access_token'] != "",'access_token不正确'
           self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_thirdlogin_missarg(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s',(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' %e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_thirdlogin_errorarg(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '1','返回code不等于1'
                assert response['returnStatus']['errorCode'] == "104",'errorCode为101'
                assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因您的请求要求太少了。'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    # 接口1.4测试
    def test_getbindcode(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' %e)
                self.cursor.execute('rollback')
            return
        try:
           assert response['returnStatus']['status'] == '0','返回code不等于0'
           assert response['returnStatus']['errorCode'] == "",'errorCode不为空'
           assert response['returnStatus']['error'] == "",'失败原因不为空'
           assert response['data'] == {},'data不为空'
           self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_getbindcode_missarg(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
           assert response['returnStatus']['status'] == '1','返回code不等于1'
           assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
           assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
           self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    def test_getbindcode_errorarg(self):
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "phone_invalid_error",'errorCode为phone_invalid_error'
            assert response['returnStatus']['error'] == "手机号码无效。",'失败原因为手机号码无效。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
    # def test_getbindcode(self):
    #     case_getbindcode.test_getbindcode(self)
    # def test_getbindcode_missarg(self):
    #     case_getbindcode.test_getbindcode_missarg(self)
    # def test_getbindcode_errorarg(self):
    #     case_getbindcode.test_getbindcode_errorarg(self)

    #############1.5登录手机绑定######################
    def test_bindphone(self):
        testrq='{\"userNo\":\"%s\",\"phone\":\"13901234567\",\"checkCode\":\"567890\"}' %TESTUSERNO
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id = 32")
        response = self.http.post(self.test_data.request_url,  testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '0','返回code不等于0'
            assert response['returnStatus']['errorCode'] == "",'errorCode不为空'
            assert response['returnStatus']['error'] == "",'失败原因不为空'
            assert response['data']['userId'] != "",'userId不准确'
            assert response['data']['userNo'] != "",'userNo不准确'
            assert response['data']['nick'] != "",'nick不准确'
            assert response['data']['userType'] != "",'userType不准确'
            assert response['data']['portraitUrl'] != "",'portraitUrl不准确'
            assert response['data']['phone'] == "13901234567",'phone不准确'
            assert response['data']['name'] != "",'portraitUrl不准确'
            assert response['data']['newUser'] != "",'newUser不准确'
            assert response['data']['access_token'] != "",'access_token不准确'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = 32")

    def test_bindphone_missarg1(self):
        testrq1='{\"phone\":\"13901234567\",\"checkCode\":\"567890\"}'
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url,  testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_bindphone_missarg2(self):
        testrq1='{\"userNo\":\"%s\",\"checkCode\":\"567890\"}' %TESTUSERNO
        # testrq3='{\"userNo\":\"%s\",\"phone\":\"13901234567\"}' %TESTUSERNO
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url,testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_bindphone_missarg3(self):
        testrq1='{\"userNo\":\"%s\",\"phone\":\"13901234567\"}' %TESTUSERNO
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url,  testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)


    def test_bindphone_erroruserno(self):
        testrq1='{\"userNo\":\"test^\",\"phone\":\"13901234567\",\"checkCode\":\"567890\"}'
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "101",'errorCode不为101'
            assert response['returnStatus']['error'] == "不给力啊。",'失败原因不为不给力啊。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)


    def test_bindphone_errorphone(self):
        testrq1='{\"userNo\":\"%s^\",\"phone\":\"1212#$\",\"checkCode\":\"567890\"}' %TESTUSERNO
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "phone_invalid_error",'errorCode不为phone_invalid_error'
            assert response['returnStatus']['error'] == "手机号码无效。",'失败原因不为手机号码无效。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_bindphone_errorcode(self):
        testrq1='{\"userNo\":\"%s^\",\"phone\":\"13901234567\",\"checkCode\":\"!@#a1\"}' %TESTUSERNO
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "bind_code_error",'errorCode不为bind_code_error'
            assert response['returnStatus']['error'] == "验证码有误，请重新输入。",'失败原因不为验证码有误，请重新输入。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    #############1.6添加用户基本信息######################
    def test_addinfo(self):
        testrq='{\"userNo\":\"%s\",\"sex\":\"M\",\"name\":\"testapi\"}' %TESTUSERNO
        # print (testrq)
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"' WHERE case_id =%s" %self.test_data.case_id)
        # print (self.test_data.request_param)
        response = self.http.post(self.test_data.request_url, testrq)
        global TESTTOKEN
        TESTTOKEN = str(response['data']['access_token'])
        print(TESTTOKEN)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        #保存TOKEN
        # print(response['data']['access_token'])
        try:
            assert response['returnStatus']['status'] == '0','返回code不等于0'
            assert response['returnStatus']['errorCode'] == "",'errorCode不为空'
            assert response['returnStatus']['error'] == "",'失败原因不为空'
            assert response['data']['userId'] != "",'userId不准确'
            assert response['data']['userNo'] != "",'userNo不准确'
            assert response['data']['nick'] != "",'nick不准确'
            assert response['data']['userType'] != "",'userType不准确'
            assert response['data']['portraitUrl'] != "",'portraitUrl不准确'
            assert response['data']['phone'] == "13901234567",'phone不准确'
            assert response['data']['name'] != "",'portraitUrl不准确'
            assert response['data']['thirdPlatform'] == "",'thirdPlatform不准确'
            assert response['data']['openId'] == "",'openId不准确'
            assert response['data']['access_token'] != "",'access_token不准确'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_addinfo_missarg1(self):
        testrq1='{\"sex\":\"F\",\"name\":\"test\"}'
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_addinfo_missarg2(self):
        testrq1='{\"userNo\":\"002559480001\",\"name\":\"test\"}'
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_addinfo_missarg3(self):
        testrq1='{\"userNo\":\"002559480001\",\"sex\":\"F\"}'
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq1+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq1)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_addinfo_erroruserno(self):
        testrq='{\"userNo\":\"1212#@!q\",\"sex\":\"F\",\"name\":\"test\"}'
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "101",'errorCode不为101'
            assert response['returnStatus']['error'] == "不给力啊。",'失败原因不为不给力啊。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_addinfo_errorsex(self):
        testrq='{\"userNo\":\"002559480001\",\"sex\":\"F\",\"name\":\"test\"}'
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s',(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为101'
            assert response['returnStatus']['error'] == "不给力啊。",'失败原因不为不给力啊。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

        ##
    def test_addinfo_errorname(self):
        testrq='{\"userNo\":\"002559480001\",\"sex\":\"M\",\"name\":\"1212qa\"}'
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为101'
            assert response['returnStatus']['error'] == "不给力啊。",'失败原因不为不给力啊。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    #############1.7修改用户基本信息######################
    def test_updateinfo(self):

        testrq='{\"access_token\":\"%s\",\"sex\":\"M\",\"name\":\"testapi\"}' %TESTTOKEN
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        #保存TOKEN
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        try:
            assert response['returnStatus']['status'] == '0','返回code不等于0'
            assert response['returnStatus']['errorCode'] == "",'errorCode不为空'
            assert response['returnStatus']['error'] == "",'失败原因不为空'
            assert response['data']['userId'] != "",'userId不准确'
            assert response['data']['userNo'] != "",'userNo不准确'
            assert response['data']['nick'] != "",'nick不准确'
            assert response['data']['userType'] != "",'userType不准确'
            assert response['data']['portraitUrl'] != "",'portraitUrl不准确'
            assert response['data']['phone'] == "13901234567",'phone不准确'
            assert response['data']['name'] != "",'portraitUrl不准确'
            assert response['data']['thirdPlatform'] != "",'thirdPlatform不准确'
            assert response['data']['openId'] != "",'openId不准确'
            assert response['data']['access_token'] != "",'access_token不准确'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        # global TESTTOKEN_NEW
        # TESTTOKEN_NEW=str(response['data']['access_token'])
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_updateinfo_missarg1(self):
        testrq='{\"access_token\":\"%s\",\"name\":\"testapi\"}' %TESTTOKEN
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_updateinfo_missarg2(self):
        testrq='{\"access_token\":\"%s\",\"sex\":\"M\"}' %TESTTOKEN
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_updateinfo_missarg3(self):
        testrq='{\"access_token\":\"%s\",\"sex\":\"M\",\"name\":\"testapi\"}' %TESTTOKEN
        # for testrq in {testrq1,testrq2,testrq3}:
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '1','返回code不等于1'
            assert response['returnStatus']['errorCode'] == "104",'errorCode不为104'
            assert response['returnStatus']['error'] == "您的请求要求太少了。",'失败原因不为您的请求要求太少了。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_updateinfo_errortoken(self):
        testrq='{\"access_token\":\"testerrortoken@_@\",\"sex\":\"M\",\"name\":\"testapi\"}'
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "token_invalid_error",'errorCode不为token_invalid_error'
            assert response['returnStatus']['error'] == "令牌失效。",'失败原因不为令牌失效。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    def test_updateinfo_errorsexname(self):
        testrq='{\"access_token\":\"%s\",\"sex\":\"aaaaa\",\"name\":\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"}' %TESTTOKEN
        # testrq='{\"access_token\":\"asas\",\"sex\":\"aaaaa\",\"name\":\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"}'
        # self.db1_cursor.execute("UPDATE test_data SET request_param ='"+testrq+"'WHERE case_id =%s" %self.test_data.case_id)
        response = self.http.post(self.test_data.request_url, testrq)
        if {} == response:
            self.test_data.result = 'Error'
            try:
        # 更新结果表中的用例运行结果
                self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                self.cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.cursor.execute('rollback')
            return
        try:
            assert response['returnStatus']['status'] == '2','返回code不等于2'
            assert response['returnStatus']['errorCode'] == "token_invalid_error",'errorCode不为token_invalid_error'
            assert response['returnStatus']['error'] == "令牌失效。",'失败原因不为令牌失效。'
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' %e)
            self.test_data.result = 'Fail'
            self.test_data.reason = '%s' %e  # 记录失败原因
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)
        self.db1_cursor.execute("UPDATE test_data SET request_param = null WHERE case_id = %s" %self.test_data.case_id)

    ##############2.1默认方案列表#################
    def test_scheme(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回code不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']['schemeList']!="",'schemelist出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    ##############2.2筛选条件#################
    def test_schemefilter(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回code不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']['filter']!="",'filter出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    ##############2.16删除评论#################
    # def test_commentdelete(self):
    #     try:
    #         testrq='{\"access_token\":\"%s\"}' %TESTTOKEN
    #         print(TESTTOKEN)
    #         response = self.http.get(self.test_data.request_url, testrq)
    #         if {} == response:
    #             self.test_data.result = 'Error'
    #             try:
    #                 self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
    #                 self.cursor.execute('commit')
    #             except Exception as e:
    #                 print('%s' %e)
    #                 self.cursor.execute('rollback')
    #             return
    #         try:
    #             assert response['returnStatus']['status'] == '0','返回code不等于0'
    #             assert response['returnStatus']['errorCode'] == "",'errorCode为空'
    #             assert response['returnStatus']['error'] == "",'失败原因不为空'
    #             assert response['data']['filter']!="",'filter出问题啦！！'
    #             self.test_data.result = 'Pass'
    #         except AssertionError as e:
    #             print('%s' %e)
    #             self.test_data.result = 'Fail'
    #             self.test_data.reason = '%s' %e  # 记录失败原因
    #         except AttributeError as e1:
    #             print('%s' %e1)
    #             self.test_data.result = 'Error'
    #             self.test_data.reason = '%s' %e1  # 记录失败原因
    #     except Exception as e2:
    #         self.test_data.result = 'Error'
    #         self.test_data.reason = '%s' %e2
    #     update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)


    #######3、	筛选方案列表##############
    def test_schemelistfilter(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回code不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']['schemeList']!="",'schemeList出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    #######4、	搜索方案列表##############
    def test_schemelistsearch(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回code不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']['schemeList']!="",'schemeList出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    #######5、	单品详细信息##############
    def test_productinfo(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回status不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']!="",'data出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

    #####6、	单品门店列表：#########
    def test_productinfo(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回status不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']!="",'data出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

######7、	相同单品方案列表####
    def test_productcase(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回status不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']['caseList']!="",'data出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)


    #####8、	同类单品列表
    def test_productsimilar(self):
        try:
            response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回status不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']['productList']!="",'data出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)

#########9、	加入购物车

    def test_cartadd(self):
        try:
            testrq='{\"goodsNo\":\"D0021005700006\",\"storeNo\":\"M00210057001\",\"schemeNo\":\"C160329012\",\"access_token\":\"%s\"}' %TESTTOKEN
            response = self.http.post(self.test_data.request_url, testrq)
            if {} == response:
                self.test_data.result = 'Error'
                try:
                    self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
                    self.cursor.execute('commit')
                except Exception as e:
                    print('%s' %e)
                    self.cursor.execute('rollback')
                return
            try:
                assert response['returnStatus']['status'] == '0','返回status不等于0'
                assert response['returnStatus']['errorCode'] == "",'errorCode为空'
                assert response['returnStatus']['error'] == "",'失败原因不为空'
                assert response['data']=="",'data出问题啦！！'
                self.test_data.result = 'Pass'
            except AssertionError as e:
                print('%s' %e)
                self.test_data.result = 'Fail'
                self.test_data.reason = '%s' %e  # 记录失败原因
            except AttributeError as e1:
                print('%s' %e1)
                self.test_data.result = 'Error'
                self.test_data.reason = '%s' %e1  # 记录失败原因
        except Exception as e2:
            self.test_data.result = 'Error'
            self.test_data.reason = '%s' %e2
        update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)



    #!!!!!!!!!!!!!!!!
    #3.10待领取列表（补贴）access_token=20160429hNyP-002559480001-jKNVCFPOvdnZO14      page=1        size=10
    # def test_order_apply(self):
    #     response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
    #     if {} == response:
    #         self.test_data.result = 'Error'
    #         try:
    #             self.cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s' ,(self.test_data.result, self.test_data.case_id))
    #             self.cursor.execute('commit')
    #         except Exception as e:
    #             print('%s' % e)
    #             self.cursor.execute('rollback')
    #         return
    #     try:
    #         assert response['returnStatus']['status'] == "0",'返回code等于0'
    #         assert response['returnStatus']['errorCode'] == "",'errorCode为空'
    #         assert response['returnStatus']['error'] == "",'error为空'
    #         assert response['data'] == {},'data不为空'
    #         self.test_data.result = 'Pass'
    #     except AssertionError as e:
    #         print('%s' %e)
    #         self.test_data.result = 'Fail'
    #         self.test_data.reason = '%s' %e  # 记录失败原因
    #     except AttributeError as e1:
    #         print('%s' %e)
    #         self.test_data.result = 'Error'
    #         self.test_data.reason = '%s' %e  # 记录失败原因
    #     update_result(self,self.test_data.case_id,self.test_data.request_param,self.test_data.result,self.test_data.reason)












    def tearDown(self):
        pass