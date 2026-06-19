# Rollback strategies for gitops-ci-cd-pipeline
#
# 1. Argo Rollouts (automatic) — canary analysis failure triggers rollback
#    kubectl argo rollouts undo gitops-app -n app-prod
#
# 2. ArgoCD (GitOps revert) — revert the image tag commit in values-*.yaml
#    argocd app rollback gitops-app-prod
#    # or: git revert <commit-sha> && git push
#
# 3. Helm (release history) — rollback to previous release revision
#    helm history gitops-app -n app-prod
#    helm rollback gitops-app <revision> -n app-prod
#
# 4. kubectl (emergency) — scale down bad revision / delete failing pods
#    kubectl rollout undo deployment/gitops-app -n app-dev
#    kubectl argo rollouts abort gitops-app -n app-prod
