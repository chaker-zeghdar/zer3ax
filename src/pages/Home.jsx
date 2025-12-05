import { useNavigate } from 'react-router-dom';
import {
  Card,
  Row,
  Col,
  Statistic,
  Table,
  Typography,
  Tag
} from 'antd';
import {
  ExperimentOutlined,
  DatabaseOutlined,
  CheckCircleOutlined,
  SyncOutlined,
  EnvironmentFilled,
  ArrowUpOutlined,
  ArrowDownOutlined
} from '@ant-design/icons';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { kpiData, recentPredictions, trendingSpecies } from '../data/mockData';

const { Title, Text } = Typography;

const Home = () => {
  const navigate = useNavigate();

  const getSuccessColor = (rate) => {
    if (rate >= 70) return 'success';
    if (rate >= 50) return 'warning';
    return 'error';
  };

  const columns = [
    {
      title: 'Plant A',
      dataIndex: 'plantA',
      key: 'plantA',
      render: (text) => <Text style={{ color: '#34495E' }}>{text.split(' ')[0]}</Text>,
    },
    {
      title: 'Plant B',
      dataIndex: 'plantB',
      key: 'plantB',
      render: (text) => <Text style={{ color: '#34495E' }}>{text.split(' ')[0]}</Text>,
    },
    {
      title: 'Success Rate',
      dataIndex: 'successRate',
      key: 'successRate',
      render: (rate) => (
        <Tag
          color={rate >= 70 ? '#2ECC71' : rate >= 50 ? '#F1C40F' : '#E74C3C'}
          style={{ borderRadius: 6, fontWeight: 600 }}
        >
          {rate}%
        </Tag>
      ),
    },
    {
      title: 'Zone',
      dataIndex: 'zone',
      key: 'zone',
      render: (text) => <Text style={{ color: '#7F8C8D' }}>{text}</Text>,
    },
  ];

  return (
    <div style={{ maxWidth: 1400, margin: '0 auto' }}>
      {/* Page Header */}
      <div style={{ marginBottom: 40 }}>
        <Title level={2} style={{ 
          color: '#2C3E50', 
          fontWeight: 700, 
          marginBottom: 8,
          fontSize: '2rem',
          letterSpacing: '-0.02em'
        }}>
          Dashboard Overview
        </Title>
        <Text style={{ color: '#7F8C8D', fontSize: '15px', fontWeight: 400 }}>
          Here's a look at your analytics and recent activity.
        </Text>
      </div>

      {/* KPI Cards */}
      <Row gutter={[20, 20]} style={{ marginBottom: 40 }}>
        <Col xs={24} sm={12} lg={8}>
          <Card
            bordered={false}
            style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid #E1E8ED',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}
          >
            <Statistic
              title={<span style={{ color: '#7F8C8D', fontSize: 13, fontWeight: 500 }}>Total Plants</span>}
              value={kpiData.totalPlants}
              valueStyle={{ color: '#2C3E50', fontSize: 32, fontWeight: 700, letterSpacing: '-0.02em' }}
              prefix={<DatabaseOutlined style={{ color: '#27AE60', fontSize: 24 }} />}
            />
            <div style={{ marginTop: 16, display: 'flex', alignItems: 'center', gap: 6 }}>
              <ArrowUpOutlined style={{ color: '#2ECC71', fontSize: 12 }} />
              <Text style={{ color: '#2ECC71', fontSize: 13, fontWeight: 600 }}>+2</Text>
              <Text style={{ color: '#95A5A6', fontSize: 12 }}>vs Previous 30 Days</Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={8}>
          <Card
            bordered={false}
            style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid #E1E8ED',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}
          >
            <Statistic
              title={<span style={{ color: '#7F8C8D', fontSize: 13, fontWeight: 500 }}>Traits Analyzed</span>}
              value={kpiData.totalTraits}
              valueStyle={{ color: '#2C3E50', fontSize: 32, fontWeight: 700, letterSpacing: '-0.02em' }}
              prefix={<ExperimentOutlined style={{ color: '#3498DB', fontSize: 24 }} />}
            />
            <div style={{ marginTop: 16, display: 'flex', alignItems: 'center', gap: 6 }}>
              <ArrowUpOutlined style={{ color: '#2ECC71', fontSize: 12 }} />
              <Text style={{ color: '#2ECC71', fontSize: 13, fontWeight: 600 }}>+12%</Text>
              <Text style={{ color: '#95A5A6', fontSize: 12 }}>vs Previous 30 Days</Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={8}>
          <Card
            bordered={false}
            style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid #E1E8ED',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}
          >
            <Statistic
              title={<span style={{ color: '#7F8C8D', fontSize: 13, fontWeight: 500 }}>Avg Success Rate</span>}
              value={kpiData.avgSuccessRate}
              suffix="%"
              valueStyle={{ color: '#2ECC71', fontSize: 32, fontWeight: 700, letterSpacing: '-0.02em' }}
              prefix={<CheckCircleOutlined style={{ color: '#2ECC71', fontSize: 24 }} />}
            />
            <div style={{ marginTop: 16, display: 'flex', alignItems: 'center', gap: 6 }}>
              <ArrowUpOutlined style={{ color: '#2ECC71', fontSize: 12 }} />
              <Text style={{ color: '#2ECC71', fontSize: 13, fontWeight: 600 }}>+5%</Text>
              <Text style={{ color: '#95A5A6', fontSize: 12 }}>vs Previous 30 Days</Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={8}>
          <Card
            bordered={false}
            style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid #E1E8ED',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}
          >
            <Statistic
              title={<span style={{ color: '#7F8C8D', fontSize: 13, fontWeight: 500 }}>Predictions Today</span>}
              value={kpiData.predictionsToday}
              valueStyle={{ color: '#2C3E50', fontSize: 32, fontWeight: 700, letterSpacing: '-0.02em' }}
              prefix={<SyncOutlined spin style={{ color: '#F1C40F', fontSize: 24 }} />}
            />
            <div style={{ marginTop: 16 }}>
              <Text style={{ color: '#95A5A6', fontSize: 12 }}>Active</Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={8}>
          <Card
            bordered={false}
            style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid #E1E8ED',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}
          >
            <Statistic
              title={<span style={{ color: '#7F8C8D', fontSize: 13, fontWeight: 500 }}>Top Zone Today</span>}
              value={kpiData.topZoneToday}
              valueStyle={{ color: '#2C3E50', fontSize: 28, fontWeight: 700, letterSpacing: '-0.02em' }}
              prefix={<EnvironmentFilled style={{ color: '#27AE60', fontSize: 24 }} />}
            />
            <div style={{ marginTop: 16 }}>
              <Text style={{ color: '#95A5A6', fontSize: 12 }}>Most popular</Text>
            </div>
          </Card>
        </Col>
      </Row>

      {/* Recent Activity */}
      <Row gutter={[20, 20]} style={{ marginBottom: 32 }}>
        <Col xs={24} lg={12}>
          <Card
            title={<span style={{ color: '#2C3E50', fontSize: 17, fontWeight: 600 }}>Last 5 Predictions</span>}
            bordered={false}
            style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid #E1E8ED',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}
          >
            <Table
              dataSource={recentPredictions}
              columns={columns}
              pagination={false}
              size="small"
              rowKey="id"
            />
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card
            title={<span style={{ color: '#2C3E50', fontSize: 17, fontWeight: 600 }}>Trending Species This Week</span>}
            bordered={false}
            style={{
              background: '#FFFFFF',
              borderRadius: 16,
              border: '1px solid #E1E8ED',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}
          >
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={trendingSpecies}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E1E8ED" />
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 11, fill: '#7F8C8D' }}
                  angle={-15}
                  textAnchor="end"
                  height={80}
                  stroke="#E1E8ED"
                />
                <YAxis tick={{ fontSize: 12, fill: '#7F8C8D' }} stroke="#E1E8ED" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#FFFFFF',
                    border: '1px solid #E1E8ED',
                    borderRadius: 8,
                    color: '#2C3E50',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
                  }}
                />
                <Bar dataKey="uses" fill="#27AE60" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Home;
