class Field(object):
    print("Field")
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
        print("<<%s" % self.name)

    def __str__(self):
        return '<%s:%s>' %(self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class ModelMetaclass(type):
    print("Meta_start")

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            print("<Created a model instance class>")
            print('>>Found model: \n1: %s, \n2: %s, \n3: %s\n' % (name, bases, attrs))
            return type.__new__(cls, name, bases, attrs)

        print("<Created a User instance class>")
        print('>>Found model: %s' % cls)
        print('>>Found model: \n1: %s, \n2: %s, \n3: %s\n' % (name, bases, attrs))

        # 下面代码目的：
        # 把attr属性内的与Field类相关的k-v对儿，集中放到mappings内，mappings放到attrs内。
        mappings = dict()
        for k, v in attrs.items(): # 找到值是Field类的对象的k-v对儿，然后复制到mappings字典内。
            if isinstance(v, Field):
                print('>>>>Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys(): # 从attr中删除值是Field类的对象的k-v对儿。
            attrs.pop(k)

        attrs['__mappings__'] = mappings  #保存属性和列的映射关系。
        attrs['__table__'] = name    #假设表的名字等于类的名字。
        return type.__new__(cls, name, bases, attrs)

    print("Meta_end")

class Model(dict, metaclass=ModelMetaclass):
    print("Model_start")
    def __init__(self, **kw):
        print("\ninit_Model: <%s>" % (self))
        super(Model, self).__init__(**kw)  #不了解这一步的实现？？？
        print("\ninit_Model: <%s>" % (self))


    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise  AttributeError(r"'Model' object has no attribute '%s'" % key )

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            print(v)
            args.append(getattr(self, k, None))
        # 通过表名来制造sql中的语句，INSERT语句。
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print("SQL: %s" % sql)
        print("ARGS: %s" % str(args))

    print('Model_end')

class User(Model):
    print("User_start")
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
    print("User_end")

# 创建一个实例：
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
print(isinstance(u, User))  #True
print(u)
# 保存到数据库：
u.save()
