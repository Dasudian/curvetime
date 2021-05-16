from django.urls import path

from curvetime.bc import node

urlpatterns = [
        path('transaction', node.Transaction.as_view()),
        path('chain', node.Chain.as_view()),
        path('mine', node.Mine.as_view()),
        path('register_node', node.Register.as_view()),
        path('register_with', node.RegisterWith.as_view()),
        path('add_block', node.Block.as_view()),
        path('pending_tx', node.Pending.as_view()),
        ]
