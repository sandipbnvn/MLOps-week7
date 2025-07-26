# MLOps Week 7 - Iris Classification API with Observability

A production-ready machine learning API for Iris flower classification with comprehensive logging, tracing, and autoscaling capabilities.

## 🚀 Features

- **FastAPI-based ML API** for Iris flower classification
- **Structured logging** with JSON format
- **OpenTelemetry tracing** with Google Cloud Trace integration
- **Kubernetes deployment** with health checks and probes
- **Horizontal Pod Autoscaler (HPA)** for automatic scaling
- **GitHub Actions CI/CD** pipelines
- **Performance testing** tools

## 📁 Project Structure

```
MLOps-week7/
├── iris_fastapi.py          # Main FastAPI application
├── test.py                  # API endpoint testing script
├── perf_test.py            # Performance testing script
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── k8s/                    # Kubernetes manifests
│   ├── staging-deployment.yaml
│   ├── production-deployment.yaml
│   └── production-hpa.yaml
├── .github/workflows/      # CI/CD pipelines
│   ├── staging-deploy.yml
│   └── production-deploy.yml
└── artifacts/              # ML model artifacts
    └── model.joblib
```

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- Docker
- Google Cloud Platform account
- Kubernetes cluster (GKE)

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python iris_fastapi.py
```

### Docker Build
```bash
docker build -t iris-api .
docker run -p 8200:8200 iris-api
```

## 🚀 Deployment

### Staging Environment
```bash
# Deploy to staging
git push origin stg
```

### Production Environment
```bash
# Deploy to production
git push origin main
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Basic health check |
| `/live_check` | GET | Kubernetes liveness probe |
| `/ready_check` | GET | Kubernetes readiness probe |
| `/predict/` | POST | Iris classification prediction |

### Example Prediction Request
```bash
curl -X POST http://your-api-url/predict/ \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## 📊 Observability

### Logging
- **Structured JSON logging** for easy parsing
- **Request/response logging** with trace IDs
- **Error logging** with stack traces
- **Performance metrics** (latency, throughput)

### Tracing
- **OpenTelemetry integration** with Google Cloud Trace
- **Distributed tracing** across service calls
- **Span correlation** for request tracking

### Monitoring
- **Kubernetes probes** for health monitoring
- **Resource metrics** (CPU, memory)
- **Custom metrics** for business KPIs

## ⚡ Autoscaling

### Horizontal Pod Autoscaler (HPA)
The production environment includes automatic scaling based on CPU utilization:

```yaml
# k8s/production-hpa.yaml
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

**Scaling Behavior:**
- **Minimum**: 2 replicas (always running)
- **Maximum**: 10 replicas (peak load)
- **Trigger**: CPU utilization > 60%
- **Scale up**: When CPU usage increases
- **Scale down**: When CPU usage decreases

### Monitoring Autoscaling
```bash
# Check HPA status
kubectl get hpa -n default

# View HPA details
kubectl describe hpa demo-iris-workload-prd-hpa -n default

# Monitor pod scaling
kubectl get pods -n default -w
```

## 🧪 Testing

### API Endpoint Testing
```bash
# Run comprehensive endpoint tests
python test.py
```

**Tests include:**
- ✅ Health check endpoints
- ✅ Prediction endpoint validation
- ✅ Error handling (invalid data)
- ✅ 404 handling
- ✅ Latency measurements

### Performance Testing
```bash
# Run load testing
python perf_test.py
```

**Performance test configuration:**
- **Threads**: 4
- **Concurrent connections**: 100
- **Duration**: 30 seconds
- **Target**: `/predict` endpoint

**Metrics measured:**
- Total requests processed
- Success/failure rates
- Latency statistics (mean, median, 99th percentile)
- Throughput (requests per second)

### Manual Testing
```bash
# Single request test
curl -X POST http://34.66.9.111/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## 🔍 Monitoring and Debugging

### View Logs
```bash
# Kubernetes logs
kubectl logs -f deployment/demo-iris-workload-prd -n default

# Google Cloud Logging
gcloud logging read "resource.type=k8s_container" --limit=50
```

### View Traces
- **Google Cloud Console** → Trace → Trace List
- Filter by service name or trace ID

### Check Service Status
```bash
# Service information
kubectl get service iris-api-service-prd -n default

# Pod status
kubectl get pods -n default -l app=iris-api
```

## 🔐 Security

### Workload Identity
- **No service account keys** stored in containers
- **Automatic authentication** via Workload Identity
- **Least privilege** IAM roles

### Required Permissions
- `roles/logging.logWriter` - Cloud Logging access
- `roles/cloudtrace.agent` - Cloud Trace access

## 📈 Performance Optimization

### Resource Limits
```yaml
resources:
  requests:
    cpu: "200m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### Scaling Recommendations
- **CPU threshold**: 60% (good balance between responsiveness and cost)
- **Memory monitoring**: Watch for memory pressure
- **Custom metrics**: Consider scaling on business metrics

## 🚨 Troubleshooting

### Common Issues

1. **Service not responding**
   - Check pod status: `kubectl get pods`
   - Check logs: `kubectl logs <pod-name>`
   - Verify service: `kubectl get svc`

2. **HPA not scaling**
   - Check HPA status: `kubectl describe hpa`
   - Verify metrics: `kubectl top pods`
   - Check resource requests/limits

3. **Logging issues**
   - Verify service account permissions
   - Check Cloud Logging console
   - Validate JSON log format

4. **Tracing issues**
   - Verify Cloud Trace API is enabled
   - Check service account has trace permissions
   - Validate OpenTelemetry configuration

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes HPA Documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [OpenTelemetry Documentation](https://opentelemetry.io/)
- [Google Cloud Trace](https://cloud.google.com/trace)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 